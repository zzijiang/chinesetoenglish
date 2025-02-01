from flask import Flask, render_template, request, jsonify, session
from random import choice
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # 用于session加密

# 定义单词表
WORD_LIST = {
    "apple": "苹果",
    "banana": "香蕉",
    "orange": "橙子",
    "grape": "葡萄",
    "pear": "梨子",
    "watermelon": "西瓜",
    "peach": "桃子",
    "cherry": "樱桃",
    "strawberry": "草莓",
    "blueberry": "蓝莓"
}

def generate_question():
    """生成随机题目"""
    chinese = choice(list(WORD_LIST.values()))
    english = [k for k, v in WORD_LIST.items() if v == chinese][0]
    return chinese, english

@app.route('/')
def index():
    """首页路由"""
    # 初始化或重置会话数据
    session['score'] = 0
    session['question_number'] = 0
    chinese, english = generate_question()
    session['current_word'] = {'chinese': chinese, 'english': english}
    return render_template('index.html')

@app.route('/check_answer', methods=['POST'])
def check_answer():
    """检查答案路由"""
    user_answer = request.json.get('answer', '').strip().lower()
    correct_answer = session['current_word']['english'].lower()
    is_correct = user_answer == correct_answer
    
    if is_correct:
        session['score'] = session.get('score', 0) + 1
    
    session['question_number'] = session.get('question_number', 0) + 1
    
    response = {
        'correct': is_correct,
        'correctAnswer': correct_answer,
        'score': session['score'],
        'questionNumber': session['question_number'],
        'gameOver': session['question_number'] >= 10
    }
    
    if session['question_number'] < 10:
        chinese, english = generate_question()
        session['current_word'] = {'chinese': chinese, 'english': english}
        response['nextWord'] = chinese
    
    return jsonify(response)

@app.route('/get_current_word')
def get_current_word():
    """获取当前题目"""
    return jsonify({
        'chinese': session['current_word']['chinese'],
        'questionNumber': session.get('question_number', 0) + 1,
        'score': session.get('score', 0)
    })

if __name__ == '__main__':
    app.run(debug=True)