from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import User, AssessmentAnswer, AssessmentSummary
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
    user_id = get_jwt_identity()

    existing = AssessmentSummary.query.filter_by(user_id=user_id).first()
    if existing:
        return jsonify({'code': 200, 'can_take': False, 'already_completed': True})

    from routes.study import get_study_day
    study_day = get_study_day(user_id)

    if study_day == 5:
        return jsonify({'code': 200, 'can_take': True, 'already_completed': False})

    return jsonify({'code': 200, 'can_take': False, 'already_completed': False})

@assessment_bp.route('/assessment/questions', methods=['GET'])
@jwt_required()
def get_questions():
    """获取测评题目"""
    words_data = load_words_json()
    day1_5_words = []
    for day_data in words_data[:5]:
        for word in day_data['words']:
            day1_5_words.append({
                'french': word['french'],
                'chinese': word['chinese'],
                'audio': f"/static/audio/{word['audio']}"
            })

    all_chinese = [w['chinese'] for w in day1_5_words]

    questions = []
    for i, word in enumerate(day1_5_words):
        options = random.sample([c for c in all_chinese if c != word['chinese']], 3)
        options.append(word['chinese'])
        random.shuffle(options)

        questions.append({
            'id': i + 1,
            'french': word['french'],
            'options': options,
            'audio_url': word['audio']
        })

    random.shuffle(questions)

    return jsonify({'code': 200, 'questions': questions})

@assessment_bp.route('/assessment/submit', methods=['POST'])
@jwt_required()
def submit_assessment():
    """提交测评答案"""
    user_id = get_jwt_identity()
    data = request.get_json()
    answers = data.get('answers', [])

    words_data = load_words_json()
    word_map = {}
    for day_data in words_data[:5]:
        for word in day_data['words']:
            word_map[word['french']] = word['chinese']

    correct_count = 0
    total_count = len(answers)

    for answer in answers:
        question_id = answer['question_id']
        user_choice = answer['user_choice']

        questions_res = get_questions()
        question = next((q for q in questions_res.json['questions'] if q['id'] == question_id), None)
        if not question:
            continue

        correct = question['options'][question['options'].index(user_choice)] == user_choice

        if correct:
            correct_count += 1

        record = AssessmentAnswer(
            user_id=user_id,
            word_french=question['french'],
            correct_chinese=word_map.get(question['french'], ''),
            user_choice=user_choice,
            is_correct=correct
        )
        db.session.add(record)

    db.session.commit()

    vocab_score = (correct_count / total_count) * 100 if total_count > 0 else 0

    summary = AssessmentSummary(
        user_id=user_id,
        vocab_score=vocab_score,
        pronunciation_avg=None,
        total_score=vocab_score
    )
    db.session.add(summary)
    db.session.commit()

    return jsonify({
        'code': 200,
        'vocab_score': round(vocab_score, 1),
        'pronunciation_avg': None,
        'total_score': round(vocab_score, 1),
        'correct_count': correct_count,
        'total_count': total_count
    })

@assessment_bp.route('/assessment/result', methods=['GET'])
@jwt_required()
def get_result():
    """获取测评结果"""
    user_id = get_jwt_identity()
    summary = AssessmentSummary.query.filter_by(user_id=user_id).first()

    if not summary:
        return jsonify({'code': 404, 'message': 'No result found'})

    return jsonify({
        'code': 200,
        'vocab_score': summary.vocab_score,
        'pronunciation_avg': summary.pronunciation_avg,
        'total_score': summary.total_score
    })