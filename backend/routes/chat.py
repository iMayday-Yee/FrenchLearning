from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime, date
from extensions import db
from models import User, DailyStatus, ChatMessage, SystemConfig
from services.llm_service import build_messages, call_llm, parse_llm_response
import json
import os
import logging
logger = logging.getLogger(__name__)

chat_bp = Blueprint('chat', __name__)

def get_study_day(user_id):
    """计算当前是第几天学习"""
    start_date_str = db.session.get(SystemConfig, 'study_start_date').value
    from datetime import date
    start = date.fromisoformat(start_date_str)
    delta = (date.today() - start).days + 1
    if delta < 1: return 0
    if delta > 12: return -1
    return delta

def get_today_status(user_id, study_day):
    """获取或创建今日学习状态"""
    today = date.today()
    status = DailyStatus.query.filter_by(user_id=user_id, study_day=study_day).first()
    if not status:
        status = DailyStatus(user_id=user_id, study_day=study_day, date=today)
        db.session.add(status)
        db.session.commit()
    return status

def load_words_json():
    """加载单词数据"""
    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_material_messages(words, study_day, base_url=''):
    """构建学习材料消息"""
    messages = []
    messages.append({"type": "text", "content": "这是今天要学习的3个法语单词，请跟着音频练习吧！"})

    for i, word in enumerate(words):
        audio_path = word['audio']
        if not audio_path.startswith('http'):
            audio_path = f"{base_url}/static/audio/{audio_path}"
        messages.append({
            "type": "word_audio",
            "content": {
                "french": word['french'],
                "chinese": word['chinese'],
                "phonetic": word.get('phonetic', ''),
                "audio_url": audio_path,
                "word_index": i
            }
        })

    messages.append({"type": "text", "content": "以上是今天的3个单词，先点击播放按钮听标准发音，然后按住麦克风按钮跟读，松开后录音会自动上传。每个单词可以多练几次！"})

    # Day 5 追加测评提醒
    if study_day == 5:
        messages.append({
            "type": "text",
            "content": "今天是第五天，测评已开启，请在完成今日学习并准备好后，向我发送\u201c开始测评\u201d获取测评内容吧！如果没有准备好也没关系，稍后我再来问问你吧！"
        })

    return messages

@chat_bp.route('/chat/send', methods=['POST'])
@jwt_required()
def send_message():
    """发送聊天消息"""
    user_id = int(get_jwt_identity())
    user = db.session.get(User, user_id)
    study_day = get_study_day(user_id)

    if study_day < 1 or study_day > 12:
        return jsonify({'code': 400, 'messages': [], 'remaining_rounds': 0})

    data = request.get_json()
    content = data.get('content', '')

    today_status = get_today_status(user_id, study_day)

    if today_status.conversation_rounds >= 20:
        return jsonify({
            'messages': [{"type": "text", "content": "今天的对话次数已用完啦，明天再来继续学习吧！"}],
            'remaining_rounds': 0
        })

    user_msg = ChatMessage(
        user_id=user_id,
        study_day=study_day,
        role='user',
        content_type='text',
        content=content
    )
    db.session.add(user_msg)
    db.session.commit()

    # 检测"开始测评"指令
    if '开始测评' in content:
        from models import AssessmentSummary
        if AssessmentSummary.query.filter_by(user_id=user_id).first():
            done_reply = "你已经完成测评了，不需要重复测评~"
            assistant_msg = ChatMessage(
                user_id=user_id, study_day=study_day,
                role='assistant', content_type='text',
                content=done_reply
            )
            db.session.add(assistant_msg)
            db.session.commit()
            return jsonify({
                'messages': [{"type": "text", "content": done_reply}],
                'remaining_rounds': 20 - today_status.conversation_rounds
            })
        if study_day == 5 and today_status.material_sent and not today_status.assessment_unlocked:
            today_status.assessment_unlocked = True
            db.session.commit()
            unlock_reply = "好的，测评已准备就绪！请点击下方的「开始测评」按钮开始吧！"
            assistant_msg = ChatMessage(
                user_id=user_id, study_day=study_day,
                role='assistant', content_type='text',
                content=unlock_reply
            )
            db.session.add(assistant_msg)
            db.session.commit()
            return jsonify({
                'messages': [{"type": "text", "content": unlock_reply}],
                'remaining_rounds': 20 - today_status.conversation_rounds
            })

    today_messages = ChatMessage.query.filter_by(
        user_id=user_id,
        study_day=study_day
    ).order_by(ChatMessage.timestamp).all()

    messages = build_messages(user, study_day, today_messages[:-1], content)

    raw_response = call_llm(messages)

    if not raw_response:
        llm_reply = "对话超时了，请重新发送试试。"
        parsed = {"intent": "other", "reply": llm_reply}
    else:
        parsed = parse_llm_response(raw_response)

    reply_text = parsed.get('reply', '好的，请继续练习吧！')
    intent = parsed.get('intent', 'other')

    # 关键词兜底：仅匹配最明确的请求，其余交给 LLM 判断
    want_material = any(kw in content for kw in ['发卡片', '发单词卡', '要学习材料'])
    accept_keywords = ['好的', '好啊', '行', '行啊', '可以', '来吧', '开始吧', '好呀', '嗯', 'ok', 'OK']
    reject_keywords = ['不了', '不用了', '不要了', '不想学', '算了', '先不了', '先别了']
    if want_material:
        intent = 'request_material'
    elif today_status.invitation_sent and not today_status.material_sent and any(kw in content for kw in accept_keywords):
        intent = 'accept_learning'
    elif today_status.invitation_sent and not today_status.material_sent and any(kw in content for kw in reject_keywords):
        intent = 'reject_learning'

    logger.warning(f"[CHAT] user={user_id} day={study_day} intent={intent} content={content[:30]} material_sent={today_status.material_sent}")

    # 用户回复了邀请但没有接受 → 清除邀请锁，下次刷新可重新邀请
    if today_status.invitation_sent and intent not in ('accept_learning', 'request_material'):
        today_status.invitation_sent = False
        db.session.commit()

    assistant_msgs = []

    if intent in ('request_material', 'accept_learning'):
        if today_status.material_sent:
            # 今天已发送过，不再重复发送
            already_reply = "今天的学习音频已经发送在上方了~可以翻看上方的单词卡片进行跟读练习！"
            assistant_msg_db = ChatMessage(
                user_id=user_id,
                study_day=study_day,
                role='assistant',
                content_type='text',
                content=already_reply
            )
            db.session.add(assistant_msg_db)
            db.session.commit()
            assistant_msgs = [{"type": "text", "content": already_reply}]
        else:
            words_data = load_words_json()
            day_words = next((d for d in words_data if d['day'] == study_day), None)
            logger.warning(f"[CHAT] {intent}: day_words={'found' if day_words else 'NONE'} for day={study_day}")
            if day_words:
                today_status.material_sent = True
                material_msgs = build_material_messages(day_words['words'], study_day, base_url=request.host_url.rstrip('/'))
                for msg in material_msgs:
                    content_type = msg['type']
                    actual_content = msg['content'] if isinstance(msg['content'], str) else json.dumps(msg['content'])
                    assistant_msg = ChatMessage(
                        user_id=user_id,
                        study_day=study_day,
                        role='assistant',
                        content_type=content_type,
                        content=actual_content
                    )
                    db.session.add(assistant_msg)
                    assistant_msgs.append(msg)
                db.session.commit()

    elif intent == 'reject_learning':
        today_status.rejected = True
        today_status.invitation_sent = False
        db.session.commit()

    elif intent == 'follow_up_practice':
        today_status.practice_count += 1
        today_status.conversation_rounds += 1
        db.session.commit()

    elif intent == 'unrelated_chat':
        # 后端直接返回固定文案，不依赖 LLM 生成
        unrelated_reply = "当前话题不在测试范围，我们只聊法语相关内容~"
        assistant_msg_db = ChatMessage(
            user_id=user_id,
            study_day=study_day,
            role='assistant',
            content_type='text',
            content=unrelated_reply
        )
        db.session.add(assistant_msg_db)
        db.session.commit()
        return jsonify({
            'messages': [{"type": "text", "content": unrelated_reply}],
            'remaining_rounds': 20 - today_status.conversation_rounds
        })

    else:
        today_status.conversation_rounds += 1
        db.session.commit()

    final_response = assistant_msgs if assistant_msgs else [{"type": "text", "content": reply_text}]

    if not assistant_msgs:
        assistant_msg_db = ChatMessage(
            user_id=user_id,
            study_day=study_day,
            role='assistant',
            content_type='text',
            content=reply_text
        )
        db.session.add(assistant_msg_db)
        db.session.commit()

    return jsonify({
        'messages': final_response,
        'remaining_rounds': 20 - today_status.conversation_rounds
    })

@chat_bp.route('/chat/history', methods=['GET'])
@jwt_required()
def get_history():
    """获取聊天记录"""
    user_id = int(get_jwt_identity())
    study_day = get_study_day(user_id)
    day = request.args.get('day', type=int) or study_day

    messages = ChatMessage.query.filter_by(
        user_id=user_id,
        study_day=day
    ).order_by(ChatMessage.timestamp).all()

    result = []
    for msg in messages:
        content = msg.content
        if msg.content_type == 'word_card':
            try:
                content = json.loads(msg.content)
            except:
                pass
        result.append({
            'id': msg.id,
            'role': msg.role,
            'type': msg.content_type,
            'content': content,
            'study_day': msg.study_day,
            'timestamp': msg.timestamp.isoformat()
        })

    return jsonify({'messages': result})

@chat_bp.route('/chat/upload_audio', methods=['POST'])
@jwt_required()
def upload_audio():
    """上传跟读录音"""
    user_id = int(get_jwt_identity())
    study_day = get_study_day(user_id)

    if study_day < 1 or study_day > 12:
        return jsonify({'code': 400, 'messages': [], 'remaining_rounds': 0})

    if 'audio' not in request.files:
        return jsonify({'code': 400, 'message': 'No audio file'}), 400

    audio_file = request.files['audio']
    word_index = request.form.get('word_index', type=int)

    from config import Config
    import time
    filename = f"{word_index or 0}_{int(time.time())}.webm"
    user_dir = os.path.join(Config.UPLOAD_FOLDER, str(user_id), str(study_day))
    os.makedirs(user_dir, exist_ok=True)
    filepath = os.path.join(user_dir, filename)
    audio_file.save(filepath)

    # 保存用户录音消息到聊天记录
    audio_url = f"/uploads/{user_id}/{study_day}/{filename}"
    user_audio_msg = ChatMessage(
        user_id=user_id,
        study_day=study_day,
        role='user',
        content_type='user_audio',
        content=audio_url
    )
    db.session.add(user_audio_msg)
    db.session.commit()

    from services.audio_service import validate_audio
    is_valid, reason = validate_audio(filepath)

    from models import AudioRecord
    audio_record = AudioRecord(
        user_id=user_id,
        study_day=study_day,
        word_index=word_index,
        target_word='',
        audio_path=filepath,
        is_valid=is_valid
    )
    db.session.add(audio_record)
    db.session.commit()

    today_status = get_today_status(user_id, study_day)

    if is_valid:
        today_status.practice_count += 1
        placeholder = f"[用户发送了单词的跟读录音]"
    else:
        today_status.invalid_audio_count += 1
        placeholder = "[该录音无效（空白/无声）]"

    today_status.conversation_rounds += 1
    db.session.commit()

    # 检查是否已超过次数限制
    if today_status.conversation_rounds >= 20:
        assistant_msg = ChatMessage(
            user_id=user_id,
            study_day=study_day,
            role='assistant',
            content_type='text',
            content='今天的对话次数已用完啦，明天再来继续学习吧！'
        )
        db.session.add(assistant_msg)
        db.session.commit()
        return jsonify({
            'messages': [{"type": "text", "content": "今天的对话次数已用完啦，明天再来继续学习吧！"}],
            'remaining_rounds': 0
        })

    today_messages = ChatMessage.query.filter_by(
        user_id=user_id,
        study_day=study_day
    ).order_by(ChatMessage.timestamp).all()

    user = db.session.get(User, user_id)
    messages = build_messages(user, study_day, today_messages, placeholder)

    raw_response = call_llm(messages)

    if raw_response:
        parsed = parse_llm_response(raw_response)
        reply_text = parsed.get('reply', '练习得不错！继续加油！')
    else:
        reply_text = '对话超时了，请重新录制试试。'

    assistant_msg = ChatMessage(
        user_id=user_id,
        study_day=study_day,
        role='assistant',
        content_type='text',
        content=reply_text
    )
    db.session.add(assistant_msg)
    db.session.commit()

    return jsonify({
        'messages': [{"type": "text", "content": reply_text}],
        'remaining_rounds': 20 - today_status.conversation_rounds
    })