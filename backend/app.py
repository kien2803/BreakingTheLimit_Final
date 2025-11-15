from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
import os

app = Flask(__name__)
CORS(app)

# Mock database
users_db = []
journals_db = []

@app.route('/api/auth/register', methods=['POST'])
def register():
    data = request.json
    user = {
        'id': len(users_db) + 1,
        'name': data['name'],
        'email': data['email'],
        'role': data.get('role', 'student'),
        'created_at': datetime.now().isoformat()
    }
    users_db.append(user)
    return jsonify({'success': True, 'user': user}), 201

@app.route('/api/auth/login', methods=['POST'])
def login():
    data = request.json
    # Mock authentication
    user = {
        'id': 1,
        'name': 'Nguyễn Văn A',
        'email': data['email'],
        'role': 'student'
    }
    token = f"mock_token_{datetime.now().timestamp()}"
    return jsonify({'token': token, 'user': user})

@app.route('/api/journal', methods=['POST'])
def create_journal():
    data = request.json
    journal = {
        'id': len(journals_db) + 1,
        'user_id': data.get('user_id', 1),
        'content': data['content'],
        'mood': data['mood'],
        'date': datetime.now().isoformat(),
        'emotion_score': None
    }
    journals_db.append(journal)
    return jsonify({'success': True, 'journal': journal}), 201

@app.route('/api/journal', methods=['GET'])
def get_journals():
    return jsonify({'journals': journals_db})

@app.route('/api/ai/analyze', methods=['POST'])
def analyze_emotion():
    data = request.json
    # Mock AI analysis
    import random
    analysis = {
        'emotionScore': {
            'positive': random.randint(40, 80),
            'neutral': random.randint(10, 40),
            'negative': random.randint(5, 25)
        },
        'wellnessScore': random.randint(60, 90),
        'suggestions': [
            'Hãy nghe một bản nhạc nhẹ nhàng',
            'Thử viết 3 điều bạn biết ơn hôm nay',
            'Đi dạo 10 phút ngoài trời'
        ],
        'sentiment': 'positive' if random.random() > 0.5 else 'neutral'
    }
    return jsonify(analysis)

@app.route('/api/activities/message/today', methods=['GET'])
def get_daily_message():
    messages = [
        'Hít thật sâu, thở ra từ từ, bạn xứng đáng được bình yên.',
        'Mỗi ngày là một khởi đầu mới, hãy tin vào bản thân.',
        'Bạn mạnh mẽ hơn bạn nghĩ. Tiếp tục tiến lên!',
        'Hãy cho phép mình được nghỉ ngơi khi cần.',
        'Niềm vui nhỏ tạo nên cuộc sống tuyệt vời.'
    ]
    import random
    message = {
        'id': random.randint(1, 1000),
        'message': random.choice(messages),
        'author': 'Breaking The Limits',
        'date': datetime.now().isoformat()
    }
    return jsonify(message)

@app.route('/api/family/children', methods=['GET'])
def get_children():
    # Mock children data
    children = [
        {
            'id': 1,
            'name': 'Nguyễn Văn An',
            'age': 16,
            'lastActive': datetime.now().isoformat(),
            'wellnessScore': 78,
            'recentMood': 'happy'
        }
    ]
    return jsonify({'children': children})

if __name__ == '__main__':
    app.run(debug=True, port=5000)