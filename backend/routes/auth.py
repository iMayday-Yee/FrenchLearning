from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from extensions import db
from models import User
from services.group_service import assign_group

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册接口"""
    data = request.get_json()

    required = ['phone', 'password', 'nickname', 'age', 'gender', 'education', 'french_interest', 'french_level', 'study_time_slot']
    for field in required:
        if not data.get(field):
            return jsonify({'code': 400, 'message': f'缺少必填字段: {field}'}), 400

    if User.query.filter_by(phone=data['phone']).first():
        return jsonify({'code': 400, 'message': '手机号已注册'}), 400

    try:
        group_type, avatar_type = assign_group(db)
    except Exception as e:
        return jsonify({'code': 500, 'message': str(e)}), 500

    user = User(
        phone=data['phone'],
        email=data.get('email'),
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

    return jsonify({'code': 200, 'user_id': user.id, 'message': '注册成功'})

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录接口"""
    data = request.get_json()
    phone = data.get('phone')
    password = data.get('password')

    if not phone or not password:
        return jsonify({'code': 400, 'message': '手机号和密码不能为空'}), 400

    user = User.query.filter_by(phone=phone).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({'code': 401, 'message': '手机号或密码错误'}), 401

    token = create_access_token(identity=user.id)
    return jsonify({'code': 200, 'token': token, 'user_id': user.id})

@auth_bp.route('/user/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """获取用户信息接口"""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'code': 404, 'message': '用户不存在'}), 404

    from config import Config
    return jsonify({
        'user_id': user.id,
        'nickname': user.nickname,
        'avatar_type': user.avatar_type,
        'avatar_url': f'/avatars/{user.avatar_type}.png',
        'study_start_date': Config.STUDY_START_DATE,
        'wechat_bound': bool(user.wechat_openid)
    })
