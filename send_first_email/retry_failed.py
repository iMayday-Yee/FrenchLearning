#!/usr/bin/env python3
"""
重发失败的邮件
- 读取 failed_emails.txt 中的地址
- 从 users.json 匹配 group_type
- 每封间隔 2 秒，带进度输出
"""
import os
import sys
import json
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP 配置（与 config.py 保持一致）
SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 465
SMTP_USER = 'hustanonymous@163.com'
SMTP_PASSWORD = 'UFdc8Gqt4hS2RUfA'

# 文件路径
BASE_DIR = os.path.dirname(__file__)
FAILED_FILE = os.path.join(BASE_DIR, 'failed_emails.txt')
USERS_JSON = os.path.join(BASE_DIR, 'users.json')


def _build_html_email(title, body_html):
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#F0F2F8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px;">
    <tr><td align="center">
      <table width="100%" style="max-width:480px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.06);">
        <tr>
          <td style="background:linear-gradient(135deg,#7B9BF4 0%,#98B2F7 100%);padding:28px 32px;text-align:center;">
            <div style="font-size:22px;font-weight:700;color:#ffffff;letter-spacing:0.5px;">{title}</div>
          </td>
        </tr>
        <tr>
          <td style="padding:32px;color:#3D4254;font-size:15px;line-height:1.7;">
            {body_html}
          </td>
        </tr>
        <tr>
          <td style="padding:20px 32px;background:#F8F9FC;border-top:1px solid #EFF1F6;text-align:center;">
            <div style="font-size:12px;color:#9096A6;">小五智能助手 · <a href="https://xiaowu.quest" style="color:#7B9BF4;text-decoration:none;">xiaowu.quest</a></div>
          </td>
        </tr>
      </table>
    </td></tr>
  </table>
</body>
</html>"""


EMAIL_BODIES = {
    'low': """欢迎参加测试！测试须知：<br><br>
1. 每天您登录小五智能助手网站后，请发送一条以下类似消息给小五。例如："发单词给我"、"我要学习"、"我准备学习法语"或"给我发送学习资料"等。小五收到消息将发送资料给您。<br><br>
2. 使用小五过程中如遇到问题，请联系：高 15827651252 或 邓 15778015561。""",

    'adjustable': """欢迎参加测试！测试须知：<br><br>
1. 每天您登录小五智能助手网站后，小五将和您交流发送当日法语学习资料情况。<br><br>
2. 使用小五过程中如遇到问题，请联系：高 15827651252 或 邓 15778015561。""",

    'high': """欢迎参加测试！测试须知：<br><br>
1. 每天您登录小五智能助手网站后，小五会发送当日的法语学习资料给您。<br><br>
2. 使用小五过程中如遇到问题，请联系：高 15827651252 或 邓 15778015561。""",
}


def load_email_to_group():
    """从 users.json 构建 email -> group_type 的映射"""
    with open(USERS_JSON, 'r', encoding='utf-8') as f:
        users = json.load(f).get('users', [])
    return {u['email']: u['group_type'] for u in users}


def load_failed_emails():
    """读取失败邮件列表"""
    with open(FAILED_FILE, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def send_email(to_email, group_type):
    """发送单封邮件，返回 (success, message)"""
    title = "小五智能助手测试须知"
    body_html = EMAIL_BODIES.get(group_type, EMAIL_BODIES['high'])

    msg = MIMEMultipart('alternative')
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = title
    plain = body_html.replace('<br>', '\n').replace('<strong>', '').replace('</strong>', '')
    msg.attach(MIMEText(plain, 'plain', 'utf-8'))
    msg.attach(MIMEText(_build_html_email(title, body_html), 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        return True, 'OK'
    except Exception as e:
        return False, str(e)


def main():
    # 加载数据
    email_to_group = load_email_to_group()
    failed_emails = load_failed_emails()
    total = len(failed_emails)

    print(f"读取到 {total} 个失败邮箱，开始重发（每封间隔 2 秒）...\n")

    success = 0
    fail = 0
    not_found = 0

    for i, email in enumerate(failed_emails, 1):
        group = email_to_group.get(email)

        if group is None:
            print(f"[{i}/{total}] ❌ {email} -> users.json 中未找到该邮箱，跳过")
            not_found += 1
            continue

        ok, result = send_email(email, group)

        if ok:
            print(f"[{i}/{total}] ✅ {email} ({group}) -> 发送成功")
            success += 1
        else:
            print(f"[{i}/{total}] ❌ {email} ({group}) -> 发送失败: {result}")
            fail += 1

        # 每封之间等待 2 秒
        if i < total:
            time.sleep(2)

        # 每 40 封暂停 3 分钟
        if i % 40 == 0 and i < total:
            print(f"\n--- 已发送 {i} 封，暂停 3 分钟 ---\n")
            time.sleep(180)

    print(f"\n===== 重发完成 =====")
    print(f"总计: {total}")
    print(f"成功: {success}")
    print(f"失败: {fail}")
    print(f"未匹配: {not_found}")


if __name__ == '__main__':
    main()
