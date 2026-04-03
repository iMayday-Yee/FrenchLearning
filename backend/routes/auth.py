import re
from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db, limiter
from models import User, SystemConfig
from services.group_service import assign_group
from services.email_service import send_verification_email, verify_code, mark_code_as_used

auth_bp = Blueprint('auth', __name__)

EMAIL_RE = re.compile(r'^[^@\s]+@[^@\s]+\.[^@\s]+$')


@auth_bp.route('/send-verification-code', methods=['POST'])
@limiter.limit("30 per hour")
def send_code():
    """发送邮箱验证码"""
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()

    if not email or not EMAIL_RE.match(email):
        return jsonify({'code': 400, 'message': '请输入有效的邮箱地址'}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({'code': 400, 'message': '该邮箱已注册'}), 400

    success, message = send_verification_email(email)
    if not success:
        return jsonify({'code': 400, 'message': message}), 400

    return jsonify({'code': 200, 'message': message})


@auth_bp.route('/verify-email', methods=['POST'])
def verify_email():
    """验证邮箱验证码"""
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()
    code = data.get('code', '')

    if not email or not EMAIL_RE.match(email):
        return jsonify({'code': 400, 'message': '请输入有效的邮箱地址'}), 400

    if not code or len(code) != 6:
        return jsonify({'code': 400, 'message': '请输入6位验证码'}), 400

    ok, msg = verify_code(email, code)
    if not ok:
        return jsonify({'code': 400, 'message': msg}), 400

    return jsonify({'code': 200, 'message': '验证成功'})


@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    # 检查学习是否已开始（防止第11天后注册）
    start_cfg = db.session.get(SystemConfig, 'study_start_date')
    if start_cfg:
        from datetime import date
        start = date.fromisoformat(start_cfg.value)
        delta = (date.today() - start).days + 1
        if delta > 10:
            return jsonify({'code': 400, 'message': '学习已结束，暂不支持注册'}), 400

    data = request.get_json()

    required = ['email', 'phone', 'password', 'nickname', 'age', 'gender', 'education', 'french_interest', 'french_level', 'study_time_slot']
    for field in required:
        if not data.get(field):
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400

    email = data['email'].strip().lower()

    if User.query.filter_by(email=email).first():
        return jsonify({'code': 400, 'message': '该邮箱已注册'}), 400

    try:
        group_type, avatar_type = assign_group(db)
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

    user = User(
        email=email,
        phone=data['phone'],
        password_hash=generate_password_hash(data['password']),
        nickname=data['nickname'],
        age=data['age'],
        gender=data['gender'],
        education=data['education'],
        french_interest=data['french_interest'],
        french_level=data['french_level'],
        study_time_slot=data['study_time_slot'],
        group_type=group_type,
        avatar_type=avatar_type
    )
    db.session.add(user)
    db.session.commit()

    # 注册成功后标记该邮箱所有未使用的验证码为已使用
    mark_code_as_used(email)

    start_date = db.session.get(SystemConfig, 'study_start_date')
    return jsonify({'code': 200, 'user_id': user.id, 'study_start_date': start_date.value if start_date else '', 'message': '注册成功'})


@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    data = request.get_json()
    email = (data.get('email') or '').strip().lower()
    password = data.get('password')

    if not email or not password:
        return jsonify({'code': 400, 'message': '邮箱和密码不能为空'}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'code': 401, 'message': '邮箱或密码错误'}), 401

    token = create_access_token(identity=str(user.id))
    return jsonify({'code': 200, 'token': token, 'user_id': user.id})


@auth_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户信息接口"""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    start_date = db.session.get(SystemConfig, 'study_start_date')
    return jsonify({
        'user_id': user.id,
        'nickname': user.nickname,
        'avatar_type': user.avatar_type,
        'avatar_url': f'/avatars/{user.avatar_type}.png',
        'study_start_date': start_date.value if start_date else '',
        'wechat_bound': bool(user.wechat_openid)
    })
