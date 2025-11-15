from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta

family_bp = Blueprint('family', __name__)

# Mock databases
connections_db = []
encouragements_db = []
letters_db = []

@family_bp.route('/family/link', methods=['POST'])
def link_family():
    """Create a family connection request"""
    data = request.json
    
    connection = {
        'id': len(connections_db) + 1,
        'parent_id': data.get('parent_id'),
        'child_email': data.get('child_email'),
        'relationship': data.get('relationship', 'parent'),
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }
    
    connections_db.append(connection)
    
    return jsonify({
        'success': True,
        'message': 'Connection request sent',
        'connection': connection
    }), 201

@family_bp.route('/family/children', methods=['GET'])
def get_children():
    """Get all children connected to a parent"""
    parent_id = request.args.get('parent_id', 1, type=int)
    
    # Mock children data
    children = [
        {
            'id': 1,
            'name': 'Nguyễn Văn An',
            'age': 16,
            'avatar': '👦',
            'lastActive': (datetime.now() - timedelta(hours=2)).isoformat(),
            'wellnessScore': 78,
            'recentMood': 'happy',
            'alerts': 0
        },
        {
            'id': 2,
            'name': 'Nguyễn Thị Bình',
            'age': 15,
            'avatar': '👧',
            'lastActive': (datetime.now() - timedelta(hours=5)).isoformat(),
            'wellnessScore': 65,
            'recentMood': 'neutral',
            'alerts': 1
        }
    ]
    
    return jsonify({'children': children})

@family_bp.route('/family/child/<int:child_id>/summary', methods=['GET'])
def get_child_summary(child_id):
    """Get emotion summary for a specific child"""
    timeframe = request.args.get('timeframe', 'week')
    
    summary = {
        'child_id': child_id,
        'timeframe': timeframe,
        'wellness_score': 78,
        'trend': '+5',
        'journal_count': 12,
        'streak_days': 7,
        'mood_variation': 'Ổn định',
        'emotion_data': {
            'positive': [65, 70, 68, 72, 75, 73, 78],
            'neutral': [25, 20, 22, 18, 15, 20, 15],
            'negative': [10, 10, 10, 10, 10, 7, 7]
        },
        'alerts': [
            {
                'type': 'suggestion',
                'message': 'Con có vẻ hơi căng thẳng những ngày qua. Hãy rủ con đi dạo.'
            }
        ]
    }
    
    return jsonify(summary)

@family_bp.route('/family/encourage', methods=['POST'])
def send_encouragement():
    """Send encouragement message from parent to child"""
    data = request.json
    
    message = {
        'id': len(encouragements_db) + 1,
        'parent_id': data.get('parent_id'),
        'child_id': data.get('child_id'),
        'message': data.get('message'),
        'is_read': False,
        'sent_at': datetime.now().isoformat()
    }
    
    encouragements_db.append(message)
    
    return jsonify({
        'success': True,
        'message': 'Encouragement sent',
        'data': message
    })

@family_bp.route('/family/letter', methods=['POST'])
def send_letter_to_parent():
    """Send letter from child to parent (requires moderation)"""
    data = request.json
    
    letter = {
        'id': len(letters_db) + 1,
        'child_id': data.get('child_id'),
        'parent_id': data.get('parent_id'),
        'content': data.get('message'),
        'status': 'pending',
        'created_at': datetime.now().isoformat()
    }
    
    letters_db.append(letter)
    
    return jsonify({
        'success': True,
        'message': 'Letter submitted for review',
        'letter': letter
    })

@family_bp.route('/family/privacy', methods=['PUT'])
def update_privacy():
    """Update student privacy settings"""
    data = request.json
    
    settings = {
        'user_id': data.get('user_id'),
        'share_emotions': data.get('share_emotions', True),
        'alert_parents': data.get('alert_parents', True),
        'receive_messages': data.get('receive_messages', True),
        'updated_at': datetime.now().isoformat()
    }
    
    return jsonify({
        'success': True,
        'settings': settings
    })