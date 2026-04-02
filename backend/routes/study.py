from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import date
from extensions import db
from models import User, DailyStatus, ChatMessage, SystemConfig
import json
import os

study_bp = Blueprint('study', __name__)

def get_study_day(user_id):
    """计算当前是第几天学习"""
    start_date_str = db.session.get(SystemConfig, 'study_start_date').value
    start = date.fromisoformat(start_date_str)
    delta = (date.today() - start).days + 1
    if delta < 1:
        return 0
    if delta > 10:
        return -1
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

@study_bp.route('/study/status', methods=['GET'])
@jwt_required()
def get_status():
    """获取当前学习状态"""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)

    study_day = get_study_day(user_id)

    if study_day == 0:
        phase = 'not_started'
    elif study_day == -1:
        phase = 'completed'
    elif study_day == 5:
        from models import AssessmentSummary
        if not AssessmentSummary.query.filter_by(user_id=user_id).first():
            phase = 'learning'
        else:
            phase = 'learning_phase2'
    elif study_day > 5:
        phase = 'learning_phase2'
    else:
        phase = 'learning'

    if phase == 'learning' and study_day == 5:
        from models import AssessmentSummary
        if not AssessmentSummary.query.filter_by(user_id=user_id).first():
            need_assessment = True
        else:
            need_assessment = False
    else:
        need_assessment = False

    today_status = get_today_status(user_id, study_day) if 1 <= study_day <= 10 else None

    return jsonify({
        'study_day': study_day,
        'phase': phase,
        'material_sent_today': today_status.material_sent if today_status else False,
        'remaining_rounds': 20 - (today_status.conversation_rounds if today_status else 0),
        'need_assessment': need_assessment
    })

@study_bp.route('/study/enter', methods=['POST'])
@jwt_required()
def study_enter():
    """用户进入/重新进入应用事件"""
    user_id = get_jwt_identity()
    user = db.session.get(User, user_id)
    study_day = get_study_day(user_id)

    if study_day < 1 or study_day > 10:
        return jsonify({'auto_messages': []})

    today_status = get_today_status(user_id, study_day)

    if user.group_type == 'low':
        # low 组：不主动发送，等用户主动请求
        return jsonify({'auto_messages': []})

    # adjustable 组：检查是否需要发送邀请
    if user.group_type == 'adjustable':
        # 如果已发送材料，不再发送邀请
        if today_status.material_sent:
            return jsonify({'auto_messages': []})
        # 如果已发送邀请但用户未回复，不再重复发送（防抖）
        if today_status.invitation_sent:
            return jsonify({'auto_messages': []})
        # 如果之前拒绝了，发送邀请（用户想再试一次）
        if today_status.rejected:
            msg_content = "您好！您现在想要练习法语吗？我可以给您发送今天的练习音频 😊"
            today_status.invitation_sent = True
            today_status.rejected = False
            db.session.commit()
            # 保存到数据库
            msg = ChatMessage(user_id=user_id, study_day=study_day, role='assistant',
                              content_type='text', content=msg_content)
            db.session.add(msg)
            db.session.commit()
            return jsonify({'auto_messages': [{"type": "text", "content": msg_content}]})
        # 首次进入或 IDLE 状态，发送邀请
        msg_content = "您好！您现在想要练习法语吗？我可以给您发送今天的练习音频 😊"
        today_status.invitation_sent = True
        db.session.commit()
        # 保存到数据库
        msg = ChatMessage(user_id=user_id, study_day=study_day, role='assistant',
                          content_type='text', content=msg_content)
        db.session.add(msg)
        db.session.commit()
        return jsonify({'auto_messages': [{"type": "text", "content": msg_content}]})

    # high 组：自动发送学习资料
    if user.group_type == 'high':
        if today_status.material_sent:
            return jsonify({'auto_messages': []})
        # 首次进入，自动发送学习资料
        import os
        words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
        with open(words_file, 'r', encoding='utf-8') as f:
            words_data = json.load(f)
        day_words = next((d for d in words_data if d['day'] == study_day), None)
        if day_words:
            today_status.material_sent = True
            db.session.commit()
            # 构建学习资料消息
            base_url = request.host_url.rstrip('/')
            messages = []
            msg_content = "这是今天要练习的法语内容，你可以开始学习了！"
            messages.append({"type": "text", "content": msg_content})
            # 保存到数据库
            msg = ChatMessage(user_id=user_id, study_day=study_day, role='assistant',
                              content_type='text', content=msg_content)
            db.session.add(msg)
            for i, word in enumerate(day_words['words']):
                audio_path = word['audio']
                if not audio_path.startswith('http'):
                    audio_path = f"{base_url}/static/audio/{audio_path}"
                card_content = json.dumps({
                    "french": word['french'],
                    "chinese": word['chinese'],
                    "audio_url": audio_path,
                    "word_index": i
                })
                messages.append({
                    "type": "word_audio",
                    "content": {
                        "french": word['french'],
                        "chinese": word['chinese'],
                        "audio_url": audio_path,
                        "word_index": i
                    }
                })
                # 保存 word_audio 消息
                msg = ChatMessage(user_id=user_id, study_day=study_day, role='assistant',
                                  content_type='word_audio', content=card_content)
                db.session.add(msg)
            end_content = "以上是今天的3个单词，请跟着音频练习发音吧！点击每个单词旁边的🎤按钮录制你的跟读。"
            messages.append({"type": "text", "content": end_content})
            msg = ChatMessage(user_id=user_id, study_day=study_day, role='assistant',
                              content_type='text', content=end_content)
            db.session.add(msg)
            db.session.commit()
            return jsonify({'auto_messages': messages})
        return jsonify({'auto_messages': []})

    return jsonify({'auto_messages': []})

@study_bp.route('/study/words', methods=['GET'])
@jwt_required()
def get_words():
    """获取某天的单词数据"""
    day = request.args.get('day', type=int)
    if not day or day < 1 or day > 10:
        return jsonify({'code': 400, 'message': 'Invalid day'}), 400

    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        all_words = json.load(f)

    day_data = next((d for d in all_words if d['day'] == day), None)
    if not day_data:
        return jsonify({'code': 404, 'message': 'Words not found'}), 404

    return jsonify({'code': 200, 'words': day_data['words']})