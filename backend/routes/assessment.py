from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, AssessmentAnswer, AssessmentSummary, SurveyResponse
import json
import os
import random

assessment_bp = Blueprint('assessment', __name__)

def load_words_json():
    """加载单词数据"""
    words_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'words.json')
    with open(words_file, 'r', encoding='utf-8') as f:
        return json.load(f)

@assessment_bp.route('/assessment/check', methods=['GET'])
@jwt_required()
def check_assessment():
    """检查是否需要/可以进行测评"""
    user_id = int(get_jwt_identity())

    existing = AssessmentSummary.query.filter_by(user_id=user_id).first()
    if existing:
        return jsonify({'code': 200, 'can_take': False, 'already_completed': True})

    from routes.study import get_study_day
    study_day = get_study_day(user_id)

    if study_day == 5:
        return jsonify({'code': 200, 'can_take': True, 'already_completed': False})

    return jsonify({'code': 200, 'can_take': False, 'already_completed': False})

@assessment_bp.route('/assessment/survey', methods=['POST'])
@jwt_required()
def submit_survey():
    """提交问卷评分"""
    user_id = int(get_jwt_identity())

    existing = SurveyResponse.query.filter_by(user_id=user_id).first()

    data = request.get_json()

    app_rating = data.get('app_rating')
    if not app_rating or not (1 <= int(app_rating) <= 7):
        return jsonify({'code': 400, 'message': 'app_rating 无效'}), 400

    details = data.get('details', {})
    if not isinstance(details, dict):
        return jsonify({'code': 400, 'message': 'details 格式错误'}), 400

    if existing:
        existing.app_rating = int(app_rating)
        existing.details = json.dumps(details, ensure_ascii=False)
    else:
        survey = SurveyResponse(
            user_id=user_id,
            app_rating=int(app_rating),
            details=json.dumps(details, ensure_ascii=False)
        )
        db.session.add(survey)
    db.session.commit()

    return jsonify({'code': 200, 'message': '问卷提交成功'})

@assessment_bp.route('/assessment/questions', methods=['GET'])
@jwt_required()
def get_questions():
    """获取测评题目（固定题库）"""
    quiz_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'quiz.json')
    with open(quiz_file, 'r', encoding='utf-8') as f:
        questions = json.load(f)

    return jsonify({'code': 200, 'questions': questions})

@assessment_bp.route('/assessment/submit', methods=['POST'])
@jwt_required()
def submit_assessment():
    """提交测评答案"""
    user_id = int(get_jwt_identity())
    data = request.get_json()
    answers = data.get('answers', [])

    quiz_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'quiz.json')
    with open(quiz_file, 'r', encoding='utf-8') as f:
        quiz_data = json.load(f)
    word_map = {q['french']: q['answer'] for q in quiz_data}

    correct_count = 0
    total_count = len(answers)

    # 删除旧答案，重新插入
    AssessmentAnswer.query.filter_by(user_id=user_id).delete()

    for answer in answers:
        french_word = answer.get('french', '')
        user_choice = answer['user_choice']

        correct_chinese = word_map.get(french_word, '')
        is_correct = user_choice == correct_chinese

        if is_correct:
            correct_count += 1

        record = AssessmentAnswer(
            user_id=user_id,
            word_french=french_word,
            correct_chinese=correct_chinese,
            user_choice=user_choice,
            is_correct=is_correct
        )
        db.session.add(record)

    # 更新或插入 summary
    summary = AssessmentSummary.query.filter_by(user_id=user_id).first()
    if summary:
        summary.correct_count = correct_count
        summary.total_count = total_count
    else:
        summary = AssessmentSummary(
            user_id=user_id,
            correct_count=correct_count,
            total_count=total_count
        )
        db.session.add(summary)
    db.session.commit()

    return jsonify({
        'code': 200,
        'correct_count': correct_count,
        'total_count': total_count
    })

@assessment_bp.route('/assessment/pronunciation_words', methods=['GET'])
@jwt_required()
def get_pronunciation_words():
    """获取发音测评单词列表（Day1-5的全部单词）"""
    words_data = load_words_json()
    words = []
    for day_data in words_data[:5]:
        for word in day_data['words']:
            words.append({
                'french': word['french'],
                'chinese': word['chinese'],
                'phonetic': word.get('phonetic', ''),
                'audio_url': f"/static/audio/{word['audio']}"
            })
    return jsonify({'code': 200, 'words': words})

@assessment_bp.route('/assessment/upload_pronunciation', methods=['POST'])
@jwt_required()
def upload_pronunciation():
    """上传发音测评录音"""
    user_id = int(get_jwt_identity())

    if 'audio' not in request.files:
        return jsonify({'code': 400, 'message': 'No audio file'}), 400

    audio_file = request.files['audio']
    word_index = request.form.get('word_index', type=int, default=0)
    target_word = request.form.get('target_word', '')

    from config import Config
    from models import AudioRecord
    import time

    user_dir = os.path.join(Config.UPLOAD_FOLDER, str(user_id), 'assessment')
    os.makedirs(user_dir, exist_ok=True)

    # 删除该用户同一单词的旧录音（文件+记录）
    old_records = AudioRecord.query.filter_by(user_id=user_id, study_day=0, word_index=word_index).all()
    for old in old_records:
        try:
            if os.path.exists(old.audio_path):
                os.remove(old.audio_path)
        except OSError:
            pass
        db.session.delete(old)
    db.session.commit()

    filename = f"pron_{word_index}_{int(time.time())}.webm"
    filepath = os.path.join(user_dir, filename)
    audio_file.save(filepath)

    record = AudioRecord(
        user_id=user_id,
        study_day=0,
        word_index=word_index,
        target_word=target_word,
        audio_path=filepath,
        is_valid=True
    )
    db.session.add(record)
    db.session.commit()

    return jsonify({'code': 200, 'message': '录音已保存'})

@assessment_bp.route('/assessment/result', methods=['GET'])
@jwt_required()
def get_result():
    """获取测评结果"""
    user_id = int(get_jwt_identity())
    summary = AssessmentSummary.query.filter_by(user_id=user_id).first()

    if not summary:
        return jsonify({'code': 404, 'message': 'No result found'})

    return jsonify({
        'code': 200,
        'correct_count': summary.correct_count,
        'total_count': summary.total_count
    })