from flask import Blueprint, request, jsonify
from datetime import datetime
from services.ai_service import AIService

journal_bp = Blueprint('journal', __name__)

# Mock database
journals_db = []

@journal_bp.route('/journal', methods=['POST'])
def create_journal():
    """Create a new journal entry with AI analysis"""
    data = request.json
    
    # Validate input
    if not data.get('content') or not data.get('mood'):
        return jsonify({'error': 'Content and mood are required'}), 400
    
    # Analyze emotion
    analysis = AIService.analyze_emotion(data['content'], data['mood'])
    
    # Create journal entry
    journal = {
        'id': len(journals_db) + 1,
        'user_id': data.get('user_id', 1),
        'content': data['content'],
        'mood': data['mood'],
        'emotion_positive': analysis['emotionScore']['positive'],
        'emotion_neutral': analysis['emotionScore']['neutral'],
        'emotion_negative': analysis['emotionScore']['negative'],
        'wellness_score': analysis['wellnessScore'],
        'suggestions': analysis['suggestions'],
        'created_at': datetime.now().isoformat()
    }
    
    journals_db.append(journal)
    
    return jsonify({
        'success': True,
        'journal': journal,
        'analysis': analysis
    }), 201

@journal_bp.route('/journal', methods=['GET'])
def get_journals():
    """Get all journals for current user"""
    user_id = request.args.get('user_id', 1, type=int)
    timeframe = request.args.get('timeframe', 'all')
    
    user_journals = [j for j in journals_db if j['user_id'] == user_id]
    
    # Filter by timeframe if needed
    if timeframe == 'week':
        # Filter last 7 days
        pass
    elif timeframe == 'month':
        # Filter last 30 days
        pass
    
    return jsonify({
        'journals': user_journals,
        'total': len(user_journals)
    })

@journal_bp.route('/journal/<int:journal_id>', methods=['GET'])
def get_journal(journal_id):
    """Get a specific journal entry"""
    journal = next((j for j in journals_db if j['id'] == journal_id), None)
    
    if not journal:
        return jsonify({'error': 'Journal not found'}), 404
    
    return jsonify({'journal': journal})

@journal_bp.route('/journal/<int:journal_id>', methods=['PUT'])
def update_journal(journal_id):
    """Update a journal entry"""
    data = request.json
    journal = next((j for j in journals_db if j['id'] == journal_id), None)
    
    if not journal:
        return jsonify({'error': 'Journal not found'}), 404
    
    # Update fields
    if 'content' in data:
        journal['content'] = data['content']
    if 'mood' in data:
        journal['mood'] = data['mood']
        # Re-analyze if mood changed
        analysis = AIService.analyze_emotion(journal['content'], data['mood'])
        journal.update({
            'emotion_positive': analysis['emotionScore']['positive'],
            'emotion_neutral': analysis['emotionScore']['neutral'],
            'emotion_negative': analysis['emotionScore']['negative'],
            'wellness_score': analysis['wellnessScore']
        })
    
    journal['updated_at'] = datetime.now().isoformat()
    
    return jsonify({'success': True, 'journal': journal})

@journal_bp.route('/journal/<int:journal_id>', methods=['DELETE'])
def delete_journal(journal_id):
    """Delete a journal entry"""
    global journals_db
    journals_db = [j for j in journals_db if j['id'] != journal_id]
    
    return jsonify({'success': True, 'message': 'Journal deleted'})

@journal_bp.route('/journal/stats', methods=['GET'])
def get_journal_stats():
    """Get statistics for user's journals"""
    user_id = request.args.get('user_id', 1, type=int)
    timeframe = request.args.get('timeframe', 'week')
    
    user_journals = [j for j in journals_db if j['user_id'] == user_id]
    
    if not user_journals:
        return jsonify({
            'total_entries': 0,
            'average_wellness': 0,
            'mood_distribution': {},
            'emotion_trend': []
        })
    
    # Calculate stats
    total = len(user_journals)
    avg_wellness = sum(j['wellness_score'] for j in user_journals) / total
    
    mood_counts = {}
    for journal in user_journals:
        mood = journal['mood']
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    return jsonify({
        'total_entries': total,
        'average_wellness': round(avg_wellness, 1),
        'mood_distribution': mood_counts,
        'streak_days': 5,  # Calculate actual streak
        'emotion_trend': [
            {'date': j['created_at'], 'wellness': j['wellness_score']}
            for j in user_journals[-7:]  # Last 7 entries
        ]
    })