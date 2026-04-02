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
