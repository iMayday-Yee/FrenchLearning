import os
from flask import Flask
from flask_cors import CORS
from flask_compress import Compress
from extensions import db, jwt, limiter
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    app.config['COMPRESS_MIN_SIZE'] = 0
    Compress(app)
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

    from flask import send_from_directory

    @app.route('/uploads/<path:filename>')
    def serve_uploads(filename):
        response = send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        response.headers['Cache-Control'] = 'public, max-age=86400'
        return response

    from routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()
        init_system_config(app)
        init_group_slots(app)
        init_wechat_accounts(app)

    # 启动定时任务（确保只有一个进程运行 scheduler）
    # - debug 模式：只在 reloader 子进程中启动
    # - gunicorn 模式：用文件锁确保只有一个 worker 启动
    if app.debug:
        if os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
            from services.scheduler_service import init_scheduler
            init_scheduler(app)
    else:
        import fcntl
        lock_path = os.path.join(app.instance_path, '.scheduler.lock')
        try:
            lock_fd = open(lock_path, 'w')
            fcntl.flock(lock_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            from services.scheduler_service import init_scheduler
            init_scheduler(app)
            app._scheduler_lock = lock_fd  # 保持引用防止 GC 释放锁
        except (IOError, OSError):
            pass  # 其他 worker，跳过

    return app

def init_system_config(app):
    defaults = {'study_start_date': app.config['STUDY_START_DATE'], 'max_daily_rounds': '20', 'reenter_threshold_minutes': '5'}
    for key, value in defaults.items():
        if not db.session.get(SystemConfig, key):
            db.session.add(SystemConfig(key=key, value=value))
    db.session.commit()

def init_group_slots(app):
    slots = app.config['GROUP_SLOTS']
    for group_type, avatars in slots.items():
        for avatar_type, count in avatars.items():
            existing = GroupSlot.query.filter_by(group_type=group_type, avatar_type=avatar_type).first()
            if not existing:
                db.session.add(GroupSlot(group_type=group_type, avatar_type=avatar_type, max_count=count, current_count=0))
    db.session.commit()

def init_wechat_accounts(app):
    from models import WechatAccount
    if WechatAccount.query.count() == 0:
        accounts = app.config.get('WECHAT_ACCOUNTS', [])
        for i, acc in enumerate(accounts):
            if acc.get('app_id'):
                db.session.add(WechatAccount(
                    app_id=acc['app_id'],
                    app_secret=acc['app_secret'],
                    token=acc.get('token', ''),
                    template_id=acc.get('template_id', ''),
                    remark=f'初始账号{i+1}'
                ))
        db.session.commit()

from models import SystemConfig, GroupSlot, EmailVerification, WechatAccount

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
