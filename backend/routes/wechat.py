from flask import Blueprint, request, jsonify, make_response
from extensions import db, limiter
from models import User, WechatAccount
from services.wechat_service import create_qrcode, get_access_token
import xml.etree.ElementTree as ET
import time

wechat_bp = Blueprint('wechat', __name__)


def parse_xml(xml_string):
    """解析微信XML数据"""
    root = ET.fromstring(xml_string)
    return {child.tag: child.text for child in root}


def find_available_account():
    """找到第一个未满的公众号，返回 WechatAccount 或 None"""
    accounts = WechatAccount.query.filter_by(enabled=True).order_by(WechatAccount.id).all()
    for acc in accounts:
        bound_count = User.query.filter_by(wechat_account_index=acc.id).filter(User.wechat_openid.isnot(None)).count()
        if bound_count < acc.max_bindable:
            return acc
    return None


@wechat_bp.route('/get_bind_qrcode', methods=['GET'])
@limiter.limit("100 per minute")
def get_bind_qrcode():
    """获取微信绑定二维码，自动分配公众号"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id required'}), 400

    user = db.session.get(User, int(user_id))
    if not user:
        return jsonify({'code': 404, 'message': 'User not found'}), 404

    # 如果用户已绑定，直接返回已绑定状态
    if user.wechat_openid:
        return jsonify({'code': 200, 'already_bound': True})

    # 查找可用公众号
    account = find_available_account()
    if not account:
        return jsonify({
            'code': 503,
            'message': '当前公众号关注数量已达上限，请通过邮箱及时接收相关通知~'
        }), 503

    scene_str = f"bind_{user_id}"
    ticket = create_qrcode(account.id, account.app_id, account.app_secret, scene_str)

    if not ticket:
        return jsonify({'code': 500, 'message': 'Failed to create QR code'}), 500

    qr_url = f"https://mp.weixin.qq.com/cgi-bin/showqrcode?ticket={ticket}"

    # 预分配 account_index 到用户（扫码后回调会写入 openid）
    user.wechat_account_index = account.id
    db.session.commit()

    return jsonify({
        'code': 200,
        'qr_url': qr_url,
        'account_id': account.id
    })


@wechat_bp.route('/bindcheck', methods=['GET'])
@limiter.limit("200 per minute")
def bindcheck():
    """检查用户微信绑定状态"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id required'}), 400

    user = db.session.get(User, int(user_id))
    if not user:
        return jsonify({'code': 404, 'message': 'User not found'}), 404

    return jsonify({
        'code': 200,
        'bound': bool(user.wechat_openid)
    })


@wechat_bp.route('/bind_status', methods=['GET'])
@limiter.limit("200 per minute")
def bind_status():
    """查询绑定状态详细信息，用于前端判断是否可以跳过"""
    user_id = request.args.get('user_id')
    if not user_id:
        return jsonify({'code': 400, 'message': 'user_id required'}), 400

    user = db.session.get(User, int(user_id))
    if not user:
        return jsonify({'code': 404, 'message': 'User not found'}), 404

    # 已绑定
    if user.wechat_openid:
        return jsonify({'code': 200, 'status': 'bound', 'can_skip': False})

    # 未绑定，但有 account_index（说明二维码已生成）
    if user.wechat_account_index:
        return jsonify({'code': 200, 'status': 'pending', 'can_skip': True})

    # 从未分配过公众号（二维码还没生成过）
    return jsonify({'code': 200, 'status': 'init', 'can_skip': True})


@wechat_bp.route('/wechat/callback', methods=['GET', 'POST'])
def wechat_callback():
    """微信服务器回调（所有公众号共用）"""
    if request.method == 'GET':
        echostr = request.args.get('echostr')
        return echostr or ''

    # POST 请求：处理扫码事件
    xml_data = request.data.decode('utf-8')
    data = parse_xml(xml_data)

    msg_type = data.get('MsgType')
    event = data.get('Event', '')

    if msg_type == 'event' and event in ('subscribe', 'SCAN'):
        openid = data.get('FromUserName')
        event_key = data.get('EventKey') or ''

        # 新关注时微信会加 "qrscene_" 前缀
        if event_key:
            event_key = event_key.replace('qrscene_', '')
        else:
            event_key = ''

        if event_key.startswith('bind_'):
            user_id_str = event_key.replace('bind_', '')
            try:
                user = db.session.get(User, int(user_id_str))
                if user:
                    user.wechat_openid = openid
                    db.session.commit()

                    # 回复绑定成功消息
                    to_user = data.get('ToUserName', '')
                    reply_xml = f"""<xml>
<ToUserName><![CDATA[{openid}]]></ToUserName>
<FromUserName><![CDATA[{to_user}]]></FromUserName>
<CreateTime>{int(time.time())}</CreateTime>
<MsgType><![CDATA[text]]></MsgType>
<Content><![CDATA[绑定成功，您的小五智能助手专属通知已开启~]]></Content>
</xml>"""
                    response = make_response(reply_xml)
                    response.content_type = 'application/xml'
                    return response
            except (ValueError, TypeError):
                pass

    return 'success'
