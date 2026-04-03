import requests
import time

token_cache = {}

def get_access_token(account_index, app_id, app_secret):
    """获取微信access_token，支持缓存"""
    cache_key = f"wechat_token_{account_index}"
    if cache_key in token_cache:
        cached = token_cache[cache_key]
        if cached['expires_at'] > time.time():
            return cached['token']

    url = f"https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={app_id}&secret={app_secret}"
    resp = requests.get(url).json()
    token = resp.get('access_token')
    if token:
        token_cache[cache_key] = {'token': token, 'expires_at': time.time() + 7000}
    return token

def create_qrcode(account_index, app_id, app_secret, scene_str):
    """创建微信临时二维码"""
    access_token = get_access_token(account_index, app_id, app_secret)
    if not access_token:
        return None

    url = f"https://api.weixin.qq.com/cgi-bin/qrcode/create?access_token={access_token}"
    data = {"action_name": "QR_STR_SCENE", "action_info": {"scene": {"scene_str": scene_str}}}
    resp = requests.post(url, json=data).json()
    return resp.get('ticket')

def send_template_message(openid, template_id, access_token, url, data):
    """发送微信模板消息"""
    api_url = f"https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={access_token}"
    payload = {
        "touser": openid,
        "template_id": template_id,
        "url": url,
        "data": data
    }
    return requests.post(api_url, json=payload).json()


def send_study_reminder_wechat(user, study_day):
    """给用户发送微信学习提醒，返回 (success, message)"""
    if not user.wechat_openid or not user.wechat_account_index:
        return False, 'user not bound'

    from models import WechatAccount
    from extensions import db
    account = db.session.get(WechatAccount, user.wechat_account_index)
    if not account or not account.template_id:
        return False, 'account or template_id not found'

    access_token = get_access_token(account.id, account.app_id, account.app_secret)
    if not access_token:
        return False, 'failed to get access_token'

    data = {
        "keyword1": {"value": f"第 {study_day} 天"},
        "keyword2": {"value": "今日学习内容已更新，点击开始学习吧！"},
    }

    try:
        result = send_template_message(
            openid=user.wechat_openid,
            template_id=account.template_id,
            access_token=access_token,
            url="https://xiaowu.quest",
            data=data
        )
        if result.get('errcode') == 0:
            return True, 'ok'
        else:
            return False, f"wechat error: {result.get('errmsg', 'unknown')}"
    except Exception as e:
        print(f"WeChat reminder error: {e}")
        return False, str(e)
