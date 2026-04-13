#!/usr/bin/env python3
"""
批量发送分组邮件给已注册用户（按 JSON 用户名单）
用法: python batch_send_group_emails.py [--dry-run]

--dry-run: 只打印邮件内容，不实际发送
"""
import sys
import os
import json
import argparse
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ========== 配置区（需要根据实际情况修改） ==========
# SMTP 配置（建议通过环境变量传入，避免敏感信息硬编码）
SMTP_SERVER = os.environ.get('SMTP_SERVER', 'smtp.163.com')
SMTP_PORT = int(os.environ.get('SMTP_PORT', 465))
SMTP_USER = os.environ.get('SMTP_USER', 'hustanonymous@163.com')
SMTP_PASSWORD = os.environ.get('SMTP_PASSWORD', 'UFdc8Gqt4hS2RUfA')

# JSON 用户名单路径
USERS_JSON_PATH = os.path.join(os.path.dirname(__file__), 'send_first_email', 'users.json')
# =================================================


def _build_html_email(title, body_html):
    """构建统一风格的 HTML 邮件（与 email_service.py 保持一致）"""
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


def load_users(json_path):
    """从 JSON 文件加载用户列表"""
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('users', [])


def send_group_email(to_email, group_type, dry_run=False):
    """发送分组邮件"""
    title = "小五智能助手测试须知"
    body_html = EMAIL_BODIES.get(group_type, EMAIL_BODIES['high'])

    msg = MIMEMultipart('alternative')
    msg['From'] = SMTP_USER
    msg['To'] = to_email
    msg['Subject'] = title
    # 纯文本版本（去掉 HTML 标签）
    plain = body_html.replace('<br>', '\n').replace('<strong>', '').replace('</strong>', '')
    msg.attach(MIMEText(plain, 'plain', 'utf-8'))
    msg.attach(MIMEText(_build_html_email(title, body_html), 'html', 'utf-8'))

    if dry_run:
        print(f"[DRY-RUN] 发送到 {to_email} (group={group_type})")
        print(f"  标题: {title}")
        print(f"  内容: {plain[:100]}...")
        print()
        return True

    try:
        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, to_email, msg.as_string())
        return True
    except Exception as e:
        print(f"[ERROR] 发送到 {to_email} 失败: {e}")
        return False


def main():
    parser = argparse.ArgumentParser(description='批量发送分组邮件')
    parser.add_argument('--dry-run', action='store_true', help='只打印，不实际发送')
    args = parser.parse_args()

    if not os.path.exists(USERS_JSON_PATH):
        print(f"错误：找不到用户名单文件 {USERS_JSON_PATH}")
        sys.exit(1)

    users = load_users(USERS_JSON_PATH)
    print(f"共找到 {len(users)} 个用户")
    print()

    low = [u for u in users if u.get('group_type') == 'low']
    adjustable = [u for u in users if u.get('group_type') == 'adjustable']
    high = [u for u in users if u.get('group_type') == 'high']
    print(f"低组: {len(low)} 人")
    print(f"可调组: {len(adjustable)} 人")
    print(f"高组: {len(high)} 人")
    print()

    if args.dry_run:
        print("=== DRY RUN，不实际发送 ===\n")
        for i, user in enumerate(users, 1):
            email = user.get('email')
            group_type = user.get('group_type', 'high')
            if not email:
                continue
            print(f"[{i}/{total}] [DRY-RUN] {email} ({group_type})")
        print(f"\n共会发送 {total} 封邮件（模拟）")
        return

    if not SMTP_PASSWORD:
        print("错误：请设置 SMTP_PASSWORD 环境变量")
        print("示例：SMTP_PASSWORD=your_password python batch_send_group_emails.py")
        sys.exit(1)

    success = 0
    fail = 0
    total = len(users)
    for i, user in enumerate(users, 1):
        email = user.get('email')
        group_type = user.get('group_type', 'high')
        if not email:
            continue
        ok = send_group_email(email, group_type, dry_run=args.dry_run)
        if ok:
            print(f"[{i}/{total}] ✅ {email} ({group_type})")
            success += 1
        else:
            print(f"[{i}/{total}] ❌ {email} ({group_type})")
            fail += 1

        # 每封之间等待 2 秒
        if not args.dry_run and i < total:
            time.sleep(2)

        # 每 40 封暂停 3 分钟
        if not args.dry_run and i % 40 == 0 and i < total:
            print(f"\n--- 已发送 {i} 封，暂停 3 分钟 ---\n")
            time.sleep(180)

    print()
    if args.dry_run:
        print(f"共会发送 {success} 封邮件（模拟）")
    else:
        print(f"发送完成: 成功 {success}，失败 {fail}")


if __name__ == '__main__':
    main()
