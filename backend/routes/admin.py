from flask import Blueprint, request, jsonify, Response
from extensions import db
from models import User, DailyStatus, ChatMessage, AudioRecord, AssessmentSummary, GroupSlot, SystemConfig
from config import Config
import csv
import io

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    """管理员认证装饰器"""
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        admin_token = request.headers.get('Admin-Token')
        if admin_token != Config.ADMIN_PASSWORD:
            return jsonify({'code': 401, 'message': 'Unauthorized'}), 401
        return f(*args, **kwargs)
    return decorated

@admin_bp.route('/admin/login', methods=['POST'])
def admin_login():
    """管理员登录"""
    data = request.get_json()
    if data.get('username') == Config.ADMIN_USERNAME and data.get('password') == Config.ADMIN_PASSWORD:
        return jsonify({'code': 200, 'admin_token': Config.ADMIN_PASSWORD})
    return jsonify({'code': 401, 'message': 'Invalid credentials'}), 401

@admin_bp.route('/admin/dashboard', methods=['GET'])
@admin_required
def dashboard():
    """获取仪表盘统计数据"""
    total_users = User.query.count()

    group_stats = db.session.query(
        User.group_type,
        User.avatar_type,
        db.func.count(User.id)
    ).group_by(User.group_type, User.avatar_type).all()

    slots = GroupSlot.query.all()
    slot_info = [{'group_type': s.group_type, 'avatar_type': s.avatar_type, 'current': s.current_count, 'max': s.max_count} for s in slots]

    completed_assessments = AssessmentSummary.query.count()

    return jsonify({
        'code': 200,
        'total_users': total_users,
        'group_stats': [{'group_type': g[0], 'avatar_type': g[1], 'count': g[2]} for g in group_stats],
        'slots': slot_info,
        'completed_assessments': completed_assessments
    })

@admin_bp.route('/admin/users', methods=['GET'])
@admin_required
def get_users():
    """获取所有用户列表"""
    users = User.query.all()
    return jsonify({
        'code': 200,
        'users': [{
            'id': u.id,
            'nickname': u.nickname,
            'phone': u.phone,
            'group_type': u.group_type,
            'avatar_type': u.avatar_type,
            'wechat_bound': bool(u.wechat_openid),
            'created_at': u.created_at.isoformat()
        } for u in users]
    })

@admin_bp.route('/admin/export/chat', methods=['GET'])
@admin_required
def export_chat():
    """导出聊天记录CSV"""
    messages = db.session.query(
        ChatMessage, User.group_type, User.avatar_type
    ).join(User).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['user_id', 'group_type', 'avatar_type', 'study_day', 'role', 'content_type', 'content', 'timestamp'])

    for msg, group_type, avatar_type in messages:
        writer.writerow([msg.user_id, group_type, avatar_type, msg.study_day, msg.role, msg.content_type, msg.content, msg.timestamp.isoformat()])

    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=chat_export.csv'})

@admin_bp.route('/admin/export/daily', methods=['GET'])
@admin_required
def export_daily():
    """导出每日学习数据CSV"""
    statuses = DailyStatus.query.all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['user_id', 'study_day', 'date', 'material_sent', 'rejected', 'practice_count', 'invalid_audio_count', 'conversation_rounds'])

    for s in statuses:
        writer.writerow([s.user_id, s.study_day, s.date.isoformat(), s.material_sent, s.rejected, s.practice_count, s.invalid_audio_count, s.conversation_rounds])

    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=daily_export.csv'})

@admin_bp.route('/admin/export/assessment', methods=['GET'])
@admin_required
def export_assessment():
    """导出测评成绩CSV"""
    results = db.session.query(
        AssessmentSummary, User
    ).join(User).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['user_id', 'nickname', 'group_type', 'avatar_type', 'vocab_score', 'pronunciation_avg', 'total_score'])

    for summary, user in results:
        writer.writerow([user.id, user.nickname, user.group_type, user.avatar_type, summary.vocab_score, summary.pronunciation_avg, summary.total_score])

    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=assessment_export.csv'})

@admin_bp.route('/admin/config', methods=['POST'])
@admin_required
def update_config():
    """更新系统配置"""
    data = request.get_json()
    key = data.get('key')
    value = data.get('value')

    if key and value:
        config = db.session.get(SystemConfig, key)
        if config:
            config.value = value
        else:
            db.session.add(SystemConfig(key=key, value=value))
        db.session.commit()

    return jsonify({'code': 200, 'message': 'Config updated'})