from flask import Blueprint, request, jsonify
import requests
from extensions import db, limiter
from models import User
from services.wechat_service import create_qrcode, get_access_token
from config import Config
import qrcode
import io
import base64
import os
import xml.etree.ElementTree as ET

wechat_bp = Blueprint('wechat', __name__)

def parse_xml(xml_string):
    """解析微信XML数据"""
    root = ET.fromstring(xml_string)
    return {child.tag: child.text for child in root}

@wechat_bp.route('/get_bind_qrcode', methods=['GET'])
@limiter.limit("100 per minute")
def get_bind_qrcode():
    """获取微信绑定二维码"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id required'}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'code': 404, 'message': 'User not found'}), 404

    account_index = 0
    account = Config.WECHAT_ACCOUNTS[account_index]

    scene_str = f"bind_{user_id}"
    ticket = create_qrcode(account_index, account['app_id'], account['app_secret'], scene_str)

    if not ticket:
        return jsonify({'code': 500, 'message': 'Failed to create QR code'}), 500

    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}")
    img = qr.make_image(fill_color="black", back_color="white")

    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    img_base64 = base64.b64encode(buf.getvalue()).decode()

    return jsonify({
        'code': 200,
        'qrcode_image': f"data:image/png;base64,{img_base64}",
        'user_id': user_id
    })

@wechat_bp.route('/bindcheck', methods=['GET'])
@limiter.limit("200 per minute")
def bindcheck():
    """检查用户微信绑定状态"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id required'}), 400

    user = db.session.get(User, user_id)
    if not user:
        return jsonify({'code': 404, 'message': 'User not found'}), 404

    return jsonify({
        'code': 200,
        'bound': bool(user.wechat_openid)
    })

@wechat_bp.route('/wechat/callback', methods=['GET', 'POST'])
def wechat_callback():
    """微信服务器回调"""
    if request.method == 'GET':
        echostr = request.args.get('echostr')
        return echostr

    # 解析XML
    xml_data = request.data.decode('utf-8')
    data = parse_xml(xml_data)

    msg_type = data.get('MsgType')

    if msg_type == 'event':
        event = data.get('Event')
        if event == 'subscribe':
            scene_str = data.get('EventKey', '')
            if scene_str.startswith('qrscene_bind_'):
                user_id = scene_str.replace('qrscene_bind_', '')
                openid = data.get('FromUserName')

                user = db.session.get(User, int(user_id))
                if user:
                    user.wechat_openid = openid
                    user.wechat_account_index = 0
                    db.session.commit()

    return 'success'
