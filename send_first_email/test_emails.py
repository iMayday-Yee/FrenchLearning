#!/usr/bin/env python3
"""
测试邮件发送 - 只发到3个指定邮箱
"""
import os
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# SMTP 配置
SMTP_SERVER = 'smtp.163.com'
SMTP_PORT = 465
SMTP_USER = 'hustanonymous@163.com'
SMTP_PASSWORD = 'UFdc8Gqt4hS2RUfA'

# 测试邮箱
TEST_EMAILS = [
    ('2818506630@qq.com', 'high'),
    ('1142036262@qq.com', 'adjustable'),
    ('yu1142036262@gmail.com', 'low'),
]


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


def send_email(to_email, group_type):
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
        print(f"✅ 发送到 {to_email} ({group_type}) 成功")
    except Exception as e:
        print(f"❌ 发送到 {to_email} ({group_type}) 失败: {e}")


if __name__ == '__main__':
    print(f"准备发送 {len(TEST_EMAILS)} 封测试邮件...\n")
    for email, group in TEST_EMAILS:
        send_email(email, group)
    print("\n完成")
