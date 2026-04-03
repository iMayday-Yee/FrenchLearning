from extensions import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    phone = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    nickname = db.Column(db.String(50), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    education = db.Column(db.String(20), nullable=False)
    french_interest = db.Column(db.String(20), nullable=False)
    french_level = db.Column(db.String(20), nullable=False)
    study_time_slot = db.Column(db.String(10), nullable=False)
    group_type = db.Column(db.String(20), nullable=False)  # low / adjustable / high
    avatar_type = db.Column(db.String(10), nullable=False)  # human / robot
    wechat_openid = db.Column(db.String(100))
    wechat_account_index = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class DailyStatus(db.Model):
    __tablename__ = 'daily_status'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_day = db.Column(db.Integer, nullable=False)
    date = db.Column(db.Date, nullable=False)
    material_sent = db.Column(db.Boolean, default=False)
    invitation_sent = db.Column(db.Boolean, default=False)  # 是否已发送邀请
    rejected = db.Column(db.Boolean, default=False)
    practice_count = db.Column(db.Integer, default=0)
    invalid_audio_count = db.Column(db.Integer, default=0)
    conversation_rounds = db.Column(db.Integer, default=0)
    reminder_sent = db.Column(db.Boolean, default=False)
    __table_args__ = (db.UniqueConstraint('user_id', 'study_day'),)

class ChatMessage(db.Model):
    __tablename__ = 'chat_messages'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_day = db.Column(db.Integer, nullable=False)
    role = db.Column(db.String(10), nullable=False)  # user / assistant
    content_type = db.Column(db.String(20), nullable=False)  # text / word_card / audio / user_audio / system
    content = db.Column(db.Text, nullable=False)
    is_template = db.Column(db.Boolean, default=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    __table_args__ = (db.Index('idx_user_study_day', 'user_id', 'study_day'),)

class AudioRecord(db.Model):
    __tablename__ = 'audio_records'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    study_day = db.Column(db.Integer, nullable=False)
    word_index = db.Column(db.Integer)
    target_word = db.Column(db.String(50))
    audio_path = db.Column(db.String(255), nullable=False)
    is_valid = db.Column(db.Boolean, default=False)
    score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AssessmentAnswer(db.Model):
    __tablename__ = 'assessment_answers'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    word_french = db.Column(db.String(50), nullable=False)
    correct_chinese = db.Column(db.String(50), nullable=False)
    user_choice = db.Column(db.String(50), nullable=False)
    is_correct = db.Column(db.Boolean, nullable=False)
    pronunciation_score = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class AssessmentSummary(db.Model):
    __tablename__ = 'assessment_summary'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    correct_count = db.Column(db.Integer, nullable=False)
    total_count = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class SystemConfig(db.Model):
    __tablename__ = 'system_config'
    key = db.Column(db.String(50), primary_key=True)
    value = db.Column(db.Text, nullable=False)

class GroupSlot(db.Model):
    __tablename__ = 'group_slots'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    group_type = db.Column(db.String(20), nullable=False)  # low / adjustable / high
    avatar_type = db.Column(db.String(10), nullable=False)  # human / robot
    max_count = db.Column(db.Integer, nullable=False)
    current_count = db.Column(db.Integer, default=0)
    __table_args__ = (db.UniqueConstraint('group_type', 'avatar_type'),)

class EmailVerification(db.Model):
    __tablename__ = 'email_verifications'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, index=True)
    code = db.Column(db.String(6), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    used = db.Column(db.Boolean, default=False)

class WechatAccount(db.Model):
    __tablename__ = 'wechat_accounts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    app_id = db.Column(db.String(100), nullable=False)
    app_secret = db.Column(db.String(100), nullable=False)
    token = db.Column(db.String(100), nullable=False)
    template_id = db.Column(db.String(200), default='')
    max_bindable = db.Column(db.Integer, default=19)
    remark = db.Column(db.String(100), default='')
    enabled = db.Column(db.Boolean, default=True)
