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
    if existing:
        return jsonify({'code': 400, 'message': '问卷已提交过'}), 400

    data = request.get_json()
    fields = ['satisfaction', 'helpfulness', 'content_quality', 'ease_of_use', 'willingness']
    for f in fields:
        v = data.get(f)
        if not v or not (1 <= int(v) <= 5):
            return jsonify({'code': 400, 'message': f'评分项 {f} 无效'}), 400

    survey = SurveyResponse(
        user_id=user_id,
        satisfaction=int(data['satisfaction']),
        helpfulness=int(data['helpfulness']),
        content_quality=int(data['content_quality']),
        ease_of_use=int(data['ease_of_use']),
        willingness=int(data['willingness'])
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

    db.session.commit()

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