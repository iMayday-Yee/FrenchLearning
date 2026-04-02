import os
from flask import Flask
from flask_cors import CORS
from extensions import db, jwt, limiter
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(app, resources={r"/api/*": {"origins": "*"}})
    db.init_app(app)
    jwt.init_app(app)
    limiter.init_app(app)

    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(app.config['AUDIO_FOLDER'], exist_ok=True)

    from routes import register_routes
    register_routes(app)

    with app.app_context():
        db.create_all()
        init_system_config(app)
        init_group_slots(app)

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

from models import SystemConfig, GroupSlot

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
