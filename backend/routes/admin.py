from flask import Blueprint, request, jsonify, Response
from extensions import db
from models import User, DailyStatus, ChatMessage, AudioRecord, AssessmentSummary, SurveyResponse, GroupSlot, SystemConfig, WechatAccount
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


@admin_bp.route('/admin/user_stats', methods=['GET'])
@admin_required
def get_user_stats():
    """获取所有用户的学习详情统计"""
    # 获取所有用户及其每日状态
    users = User.query.all()
    daily_statuses = DailyStatus.query.all()

    # 按 user_id 分组
    status_by_user = {}
    for ds in daily_statuses:
        if ds.user_id not in status_by_user:
            status_by_user[ds.user_id] = {}
        status_by_user[ds.user_id][ds.study_day] = {
            'material_sent': ds.material_sent,
            'rejected': ds.rejected,
            'practice_count': ds.practice_count,
            'invalid_audio_count': ds.invalid_audio_count,
            'conversation_rounds': ds.conversation_rounds,
            'date': ds.date.isoformat() if ds.date else None
        }

    # 计算统计
    total_practice = sum(ds.practice_count for ds in daily_statuses)
    total_invalid = sum(ds.invalid_audio_count for ds in daily_statuses)
    total_rounds = sum(ds.conversation_rounds for ds in daily_statuses)
    # 有多少人至少收到过一次材料
    users_with_material = len(set(ds.user_id for ds in daily_statuses if ds.material_sent))
    # 有多少人至少拒绝过一次
    users_who_rejected = len(set(ds.user_id for ds in daily_statuses if ds.rejected))

    result = []
    for u in users:
        user_days = status_by_user.get(u.id, {})
        # 计算该用户的学习天数（material_sent=True的天数）
        active_days = sum(1 for d in user_days.values() if d['material_sent'])
        total_prac = sum(d['practice_count'] for d in user_days.values())
        total_rnd = sum(d['conversation_rounds'] for d in user_days.values())

        # 评估成绩
        assessment = AssessmentSummary.query.filter_by(user_id=u.id).first()

        result.append({
            'user_id': u.id,
            'nickname': u.nickname,
            'email': u.email,
            'group_type': u.group_type,
            'avatar_type': u.avatar_type,
            'study_time_slot': u.study_time_slot,
            'active_days': active_days,
            'total_practice': total_prac,
            'total_rounds': total_rnd,
            'assessment_completed': assessment is not None,
            'assessment_correct': assessment.correct_count if assessment else None,
            'assessment_total': assessment.total_count if assessment else None,
            'daily_status': user_days
        })

    return jsonify({
        'code': 200,
        'stats': {
            'total_practice': total_practice,
            'total_invalid_audio': total_invalid,
            'total_conversation_rounds': total_rounds,
            'users_with_material_sent': users_with_material,
            'users_who_rejected': users_who_rejected
        },
        'users': result
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

@admin_bp.route('/admin/export/survey', methods=['GET'])
@admin_required
def export_survey():
    """导出问卷评分CSV"""
    results = db.session.query(
        SurveyResponse, User
    ).join(User).all()

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['user_id', 'nickname', 'group_type', 'avatar_type',
                     'app_rating', 'details_json', 'created_at'])

    for survey, user in results:
        writer.writerow([user.id, user.nickname, user.group_type, user.avatar_type,
                         survey.app_rating, survey.details, survey.created_at])

    return Response(output.getvalue(), mimetype='text/csv',
                    headers={'Content-Disposition': 'attachment; filename=survey_export.csv'})

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
    if day < 1 or day > 12:
        return jsonify({'code': 400, 'message': '天数必须在1-12之间'}), 400

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
        # 确保 phonetic 字段被保留（如果没有则设为空）
        if 'phonetic' not in w:
            w['phonetic'] = ''

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
    if day < 1 or day > 12:
        return jsonify({'code': 400, 'message': '天数必须在1-12之间'}), 400

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
    llm_api_key = db.session.get(SystemConfig, 'llm_api_key')
    return jsonify({
        'code': 200,
        'study_start_date': start_date.value if start_date else '',
        'llm_api_key': llm_api_key.value if llm_api_key else ''
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


@admin_bp.route('/admin/wechat_accounts', methods=['GET'])
@admin_required
def get_wechat_accounts():
    """获取所有公众号及绑定统计"""
    accounts = WechatAccount.query.order_by(WechatAccount.id).all()
    result = []
    for acc in accounts:
        bound_count = User.query.filter_by(wechat_account_index=acc.id).filter(User.wechat_openid.isnot(None)).count()
        result.append({
            'id': acc.id,
            'app_id': acc.app_id,
            'app_secret': acc.app_secret,
            'token': acc.token,
            'template_id': acc.template_id,
            'max_bindable': acc.max_bindable,
            'bound_count': bound_count,
            'remark': acc.remark,
            'enabled': acc.enabled
        })
    return jsonify({'code': 200, 'accounts': result})


@admin_bp.route('/admin/wechat_accounts', methods=['POST'])
@admin_required
def add_wechat_account():
    """添加公众号"""
    data = request.get_json()
    if not data.get('app_id') or not data.get('app_secret'):
        return jsonify({'code': 400, 'message': 'app_id 和 app_secret 必填'}), 400

    acc = WechatAccount(
        app_id=data['app_id'],
        app_secret=data['app_secret'],
        token=data.get('token', ''),
        template_id=data.get('template_id', ''),
        max_bindable=data.get('max_bindable', 19),
        remark=data.get('remark', ''),
        enabled=data.get('enabled', True)
    )
    db.session.add(acc)
    db.session.commit()
    return jsonify({'code': 200, 'message': '添加成功', 'id': acc.id})


@admin_bp.route('/admin/wechat_accounts/<int:account_id>', methods=['PUT'])
@admin_required
def update_wechat_account(account_id):
    """编辑公众号"""
    acc = db.session.get(WechatAccount, account_id)
    if not acc:
        return jsonify({'code': 404, 'message': '公众号不存在'}), 404

    data = request.get_json()
    if 'app_id' in data: acc.app_id = data['app_id']
    if 'app_secret' in data: acc.app_secret = data['app_secret']
    if 'token' in data: acc.token = data['token']
    if 'template_id' in data: acc.template_id = data['template_id']
    if 'max_bindable' in data: acc.max_bindable = data['max_bindable']
    if 'remark' in data: acc.remark = data['remark']
    if 'enabled' in data: acc.enabled = data['enabled']
    db.session.commit()
    return jsonify({'code': 200, 'message': '更新成功'})


@admin_bp.route('/admin/wechat_accounts/<int:account_id>', methods=['DELETE'])
@admin_required
def delete_wechat_account(account_id):
    """删除公众号（仅允许无绑定用户时）"""
    acc = db.session.get(WechatAccount, account_id)
    if not acc:
        return jsonify({'code': 404, 'message': '公众号不存在'}), 404

    bound_count = User.query.filter_by(wechat_account_index=acc.id).filter(User.wechat_openid.isnot(None)).count()
    if bound_count > 0:
        return jsonify({'code': 400, 'message': f'该公众号下还有 {bound_count} 个绑定用户，无法删除'}), 400

    db.session.delete(acc)
    db.session.commit()
    return jsonify({'code': 200, 'message': '删除成功'})


@admin_bp.route('/admin/wechat_accounts/<int:account_id>/users', methods=['GET'])
@admin_required
def get_wechat_account_users(account_id):
    """获取该公众号下绑定的用户列表"""
    acc = db.session.get(WechatAccount, account_id)
    if not acc:
        return jsonify({'code': 404, 'message': '公众号不存在'}), 404

    users = User.query.filter_by(wechat_account_index=account_id).filter(User.wechat_openid.isnot(None)).all()
    return jsonify({
        'code': 200,
        'users': [{'id': u.id, 'nickname': u.nickname, 'email': u.email} for u in users]
    })