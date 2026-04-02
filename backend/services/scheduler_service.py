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
        if study_day < 1 or study_day > 10:
            return

        # 只在整点后 0-4 分钟内触发
        now = datetime.now()
        if now.minute > 4:
            return

        # 当前整点对应的 time_slot，如 "22:00"
        current_slot = f"{now.hour:02d}:00"

        # 找到匹配时间段的用户
        users = User.query.filter_by(study_time_slot=current_slot).all()
        if not users:
            return

        for user in users:
            # 获取或创建今天的 DailyStatus
            status = DailyStatus.query.filter_by(user_id=user.id, study_day=study_day).first()
            if not status:
                status = DailyStatus(user_id=user.id, study_day=study_day, date=date.today())
                db.session.add(status)
                db.session.commit()

            if status.reminder_sent:
                continue

            success, msg = send_study_reminder(user.email, study_day)
            if success:
                status.reminder_sent = True
                db.session.commit()
                print(f"Reminder sent to {user.email} for day {study_day}")
            else:
                print(f"Failed to send reminder to {user.email}: {msg}")


def init_scheduler(app):
    """初始化并启动定时任务"""
    scheduler.add_job(
        func=check_and_send_reminders,
        trigger='interval',
        minutes=1,
        args=[app],
        id='study_reminder',
        misfire_grace_time=300
    )
    scheduler.start()
    print("Scheduler started: study reminder job running every minute")
