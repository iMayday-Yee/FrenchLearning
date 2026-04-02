from flask import Blueprint, request, jsonify, Response
from extensions import db
from models import User, DailyStatus, ChatMessage, AudioRecord, AssessmentSummary, GroupSlot, SystemConfig
from config import Config
import csv
import io
import json
import os

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
            'email': u.email,
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
    writer.writerow(['user_id', 'nickname', 'group_type', 'avatar_type', 'correct_count', 'total_count'])

    for summary, user in results:
        writer.writerow([user.id, user.nickname, user.group_type, user.avatar_type, summary.correct_count, summary.total_count])

    return Response(output.getvalue(), mimetype='text/csv', headers={'Content-Disposition': 'attachment; filename=assessment_export.csv'})

@admin_bp.route('/admin/words', methods=['GET'])
@admin_required
def get_words():
    """获取所有天的单词数据"""
    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        words_data = json.load(f)
    return jsonify({'code': 200, 'words': words_data})


@admin_bp.route('/admin/words/<int:day>', methods=['PUT'])
@admin_required
def update_words(day):
    """更新某天的单词数据"""
    if day < 1 or day > 10:
        return jsonify({'code': 400, 'message': '天数必须在1-10之间'}), 400

    data = request.get_json()
    words = data.get('words', [])

    if len(words) != 3:
        return jsonify({'code': 400, 'message': '每天必须有3个单词'}), 400

    for i, w in enumerate(words):
        if not w.get('french') or not w.get('chinese'):
            return jsonify({'code': 400, 'message': f'第{i+1}个单词缺少法语或中文'}), 400
        w['index'] = i + 1
        if not w.get('audio'):
            w['audio'] = f"day{day}/{day}-{i+1}.mp3"

    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        all_words = json.load(f)

    day_entry = next((d for d in all_words if d['day'] == day), None)
    if day_entry:
        day_entry['words'] = words
    else:
        all_words.append({'day': day, 'words': words})
        all_words.sort(key=lambda x: x['day'])

    with open(words_file, 'w', encoding='utf-8') as f:
        json.dump(all_words, f, ensure_ascii=False, indent=2)

    return jsonify({'code': 200, 'message': f'第{day}天单词已更新'})


@admin_bp.route('/admin/words/<int:day>/audio', methods=['POST'])
@admin_required
def upload_word_audio(day):
    """上传单词音频"""
    if day < 1 or day > 10:
        return jsonify({'code': 400, 'message': '天数必须在1-10之间'}), 400

    if 'audio' not in request.files:
        return jsonify({'code': 400, 'message': '没有音频文件'}), 400

    word_index = request.form.get('word_index', type=int)
    if not word_index or word_index < 1 or word_index > 3:
        return jsonify({'code': 400, 'message': 'word_index必须在1-3之间'}), 400

    audio_file = request.files['audio']
    audio_dir = os.path.join(Config.AUDIO_FOLDER, f'day{day}')
    os.makedirs(audio_dir, exist_ok=True)

    filename = f"{day}-{word_index}.mp3"
    filepath = os.path.join(audio_dir, filename)
    audio_file.save(filepath)

    return jsonify({'code': 200, 'message': '音频上传成功', 'audio_path': f'day{day}/{filename}'})


@admin_bp.route('/admin/config', methods=['GET'])
@admin_required
def get_config():
    """获取系统配置"""
    start_date = db.session.get(SystemConfig, 'study_start_date')
    return jsonify({
        'code': 200,
        'study_start_date': start_date.value if start_date else ''
    })


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