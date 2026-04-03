import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from config import Config
from models import EmailVerification
from extensions import db


def generate_code():
    return ''.join([str(random.randint(0, 9)) for _ in range(6)])


def _build_html_email(title, body_html):
    """构建统一风格的 HTML 邮件"""
    return f"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body style="margin:0;padding:0;background:#F0F2F8;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI','PingFang SC','Microsoft YaHei',sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="padding:40px 20px;">
    <tr><td align="center">
      <table width="100%" style="max-width:480px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 24px rgba(0,0,0,0.06);">
        <!-- Header -->
        <tr>
          <td style="background:linear-gradient(135deg,#7B9BF4 0%,#98B2F7 100%);padding:28px 32px;text-align:center;">
            <div style="font-size:22px;font-weight:700;color:#ffffff;letter-spacing:0.5px;">{title}</div>
          </td>
        </tr>
        <!-- Body -->
        <tr>
          <td style="padding:32px;color:#3D4254;font-size:15px;line-height:1.7;">
            {body_html}
          </td>
        </tr>
        <!-- Footer -->
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


def send_verification_email(email_address):
    """发送验证码邮件，返回 (success, message)"""
    cutoff = datetime.utcnow() - timedelta(seconds=Config.EMAIL_SEND_COOLDOWN_SECONDS)
    recent = EmailVerification.query.filter(
        EmailVerification.email == email_address,
        EmailVerification.created_at > cutoff
    ).first()
    if recent:
        elapsed = (datetime.utcnow() - recent.created_at).total_seconds()
        remaining = int(Config.EMAIL_SEND_COOLDOWN_SECONDS - elapsed)
        return False, f'发送过于频繁，请{remaining}秒后再试'

    # 使该邮箱之前所有未使用的验证码失效（确保只有最新一个有效）
    EmailVerification.query.filter(
        EmailVerification.email == email_address,
        EmailVerification.used == False
    ).update({'used': True})
    db.session.commit()

    code = generate_code()

    body_html = f"""
    <p style="margin:0 0 20px;">你好！</p>
    <p style="margin:0 0 24px;">你正在注册小五智能助手，请使用以下验证码完成验证：</p>
    <div style="text-align:center;margin:0 0 24px;">
      <div style="display:inline-block;padding:14px 40px;background:linear-gradient(135deg,#7B9BF4 0%,#98B2F7 100%);border-radius:12px;font-size:28px;font-weight:700;color:#ffffff;letter-spacing:8px;">{code}</div>
    </div>
    <p style="margin:0 0 8px;color:#5E6478;">验证码有效期为 <strong>{Config.EMAIL_CODE_EXPIRY_MINUTES} 分钟</strong>，请尽快使用。</p>
    <p style="margin:0;color:#9096A6;font-size:13px;">如非本人操作，请忽略此邮件。</p>
    """

    msg = MIMEMultipart('alternative')
    msg['From'] = Config.SMTP_USER
    msg['To'] = email_address
    msg['Subject'] = '小五智能助手 - 邮箱验证码'
    msg.attach(MIMEText(f'你的验证码是：{code}，有效期{Config.EMAIL_CODE_EXPIRY_MINUTES}分钟。', 'plain', 'utf-8'))
    msg.attach(MIMEText(_build_html_email('邮箱验证', body_html), 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_USER, email_address, msg.as_string())
    except Exception as e:
        print(f"SMTP error: {e}")
        return False, '邮件发送失败，请稍后重试'

    verification = EmailVerification(email=email_address, code=code)
    db.session.add(verification)
    db.session.commit()

    return True, '验证码已发送'


def send_study_reminder(email_address, study_day):
    """发送学习提醒邮件，返回 (success, message)"""
    body_html = f"""
    <p style="margin:0 0 6px;font-size:13px;color:#7B9BF4;font-weight:600;">📚 法语学习助手 · 来自小五智能助手</p>
    <p style="margin:0 0 20px;">Bonjour !</p>
    <p style="margin:0 0 8px;">今天是法语学习的<strong>第 {study_day} 天</strong>，今天的学习内容已经准备好了。</p>
    <p style="margin:0 0 28px;color:#5E6478;">点击下方按钮开始今天的学习吧！</p>
    <div style="text-align:center;margin:0 0 24px;">
      <a href="https://xiaowu.quest" style="display:inline-block;padding:12px 36px;background:linear-gradient(135deg,#7B9BF4 0%,#98B2F7 100%);border-radius:10px;font-size:15px;font-weight:600;color:#ffffff;text-decoration:none;">开始学习</a>
    </div>
    <p style="margin:0;color:#9096A6;font-size:13px;">每天坚持一点点，进步看得见。</p>
    """

    msg = MIMEMultipart('alternative')
    msg['From'] = Config.SMTP_USER
    msg['To'] = email_address
    msg['Subject'] = f'法语学习提醒 - 第{study_day}天 | 小五智能助手'
    msg.attach(MIMEText(f'[法语学习助手 · 来自小五智能助手] 今天是法语学习第{study_day}天，打开 https://xiaowu.quest 开始学习吧！', 'plain', 'utf-8'))
    msg.attach(MIMEText(_build_html_email(f'第 {study_day} 天学习提醒', body_html), 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_USER, email_address, msg.as_string())
    except Exception as e:
        print(f"SMTP reminder error: {e}")
        return False, str(e)

    return True, 'ok'


def verify_code(email_address, code):
    """校验验证码，返回 (success, message)"""
    expiry = datetime.utcnow() - timedelta(minutes=Config.EMAIL_CODE_EXPIRY_MINUTES)
    record = EmailVerification.query.filter(
        EmailVerification.email == email_address,
        EmailVerification.code == code,
        EmailVerification.used == False,
        EmailVerification.created_at > expiry
    ).order_by(EmailVerification.created_at.desc()).first()

    if not record:
        return False, '验证码错误或已过期'

    # 不在这里标记 used=True，让验证码在有效期内可以重复使用
    # （只有在注册成功后才标记为已使用，防止同一验证码用于多次注册）
    return True, '验证成功'


def mark_code_as_used(email_address):
    """标记该邮箱所有未使用的验证码为已使用（注册成功后调用）"""
    EmailVerification.query.filter(
        EmailVerification.email == email_address,
        EmailVerification.used == False
    ).update({'used': True})
    db.session.commit()


def send_reset_code_email(email_address):
    """发送密码重置验证码邮件，返回 (success, message)"""
    cutoff = datetime.utcnow() - timedelta(seconds=Config.EMAIL_SEND_COOLDOWN_SECONDS)
    recent = EmailVerification.query.filter(
        EmailVerification.email == email_address,
        EmailVerification.created_at > cutoff
    ).first()
    if recent:
        elapsed = (datetime.utcnow() - recent.created_at).total_seconds()
        remaining = int(Config.EMAIL_SEND_COOLDOWN_SECONDS - elapsed)
        return False, f'发送过于频繁，请{remaining}秒后再试'

    # 使该邮箱之前所有未使用的验证码失效
    EmailVerification.query.filter(
        EmailVerification.email == email_address,
        EmailVerification.used == False
    ).update({'used': True})
    db.session.commit()

    code = generate_code()

    body_html = f"""
    <p style="margin:0 0 20px;">你好！</p>
    <p style="margin:0 0 24px;">你正在重置小五智能助手的密码，请使用以下验证码完成验证：</p>
    <div style="text-align:center;margin:0 0 24px;">
      <div style="display:inline-block;padding:14px 40px;background:linear-gradient(135deg,#7B9BF4 0%,#98B2F7 100%);border-radius:12px;font-size:28px;font-weight:700;color:#ffffff;letter-spacing:8px;">{code}</div>
    </div>
    <p style="margin:0 0 8px;color:#5E6478;">验证码有效期为 <strong>{Config.EMAIL_CODE_EXPIRY_MINUTES} 分钟</strong>，请尽快使用。</p>
    <p style="margin:0;color:#9096A6;font-size:13px;">如非本人操作，请忽略此邮件。</p>
    """

    msg = MIMEMultipart('alternative')
    msg['From'] = Config.SMTP_USER
    msg['To'] = email_address
    msg['Subject'] = '小五智能助手 - 密码重置验证码'
    msg.attach(MIMEText(f'你的密码重置验证码是：{code}，有效期{Config.EMAIL_CODE_EXPIRY_MINUTES}分钟。', 'plain', 'utf-8'))
    msg.attach(MIMEText(_build_html_email('密码重置', body_html), 'html', 'utf-8'))

    try:
        with smtplib.SMTP_SSL(Config.SMTP_SERVER, Config.SMTP_PORT) as server:
            server.login(Config.SMTP_USER, Config.SMTP_PASSWORD)
            server.sendmail(Config.SMTP_USER, email_address, msg.as_string())
    except Exception as e:
        print(f"SMTP error: {e}")
        return False, '邮件发送失败，请稍后重试'

    verification = EmailVerification(email=email_address, code=code)
    db.session.add(verification)
    db.session.commit()

    return True, '验证码已发送'
