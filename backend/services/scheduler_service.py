from datetime import datetime, date
from apscheduler.schedulers.background import BackgroundScheduler

scheduler = BackgroundScheduler(daemon=True)


def check_and_send_reminders(app):
    """检查并发送学习提醒邮件"""
    with app.app_context():
        from models import User, DailyStatus, SystemConfig
        from extensions import db
        from services.email_service import send_study_reminder

        # 计算当前 study_day
        start_cfg = db.session.get(SystemConfig, 'study_start_date')
        if not start_cfg:
            return
        start = date.fromisoformat(start_cfg.value)
        study_day = (date.today() - start).days + 1
        if study_day < 1 or study_day > 12:
            return

        # 精确到分钟：当前时间对应的 time_slot，如 "22:30"
        now = datetime.now()
        current_slot = f"{now.hour:02d}:{now.minute:02d}"

        # 找到匹配时间段的用户
        users = User.query.filter_by(study_time_slot=current_slot).all()
        if not users:
            return

        from services.wechat_service import send_study_reminder_wechat

        for user in users:
            # 获取或创建今天的 DailyStatus
            status = DailyStatus.query.filter_by(user_id=user.id, study_day=study_day).first()
            if not status:
                status = DailyStatus(user_id=user.id, study_day=study_day, date=date.today())
                db.session.add(status)
                db.session.commit()

            if status.reminder_sent:
                continue

            # 邮件必发
            email_ok, email_msg = send_study_reminder(user.email, study_day)
            if email_ok:
                print(f"Email reminder sent to {user.email} for day {study_day}")
            else:
                print(f"Failed to send email to {user.email}: {email_msg}")

            # 绑定了微信的也必发
            if user.wechat_openid:
                wx_ok, wx_msg = send_study_reminder_wechat(user, study_day)
                if wx_ok:
                    print(f"WeChat reminder sent to user {user.id} for day {study_day}")
                else:
                    print(f"Failed to send WeChat to user {user.id}: {wx_msg}")

            # 标记已发送（不管成功失败，避免重复轰炸）
            status.reminder_sent = True
            db.session.commit()


def init_scheduler(app):
    """初始化并启动定时任务"""
    scheduler.add_job(
        func=check_and_send_reminders,
        trigger='interval',
        seconds=30,
        args=[app],
        id='study_reminder',
        misfire_grace_time=300
    )
    scheduler.start()
    print("Scheduler started: study reminder job running every 30 seconds")
