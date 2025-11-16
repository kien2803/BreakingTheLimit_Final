from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import db, Journal, User
from services.ai_service import AIService
from routes.auth import get_current_user

journal_bp = Blueprint('journal', __name__)

@journal_bp.route('/journal', methods=['POST'])
def create_journal():
    """Create a new journal entry with AI analysis"""
    data = request.json
    
    # Validate input
    if not data.get('content') or not data.get('mood'):
        return jsonify({'error': 'Content and mood are required'}), 400
    
    # Get user (from token or request)
    user_id = data.get('user_id')
    if not user_id:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User authentication required'}), 401
        user_id = user.id
    
    # Analyze emotion
    analysis = AIService.analyze_emotion(data['content'], data['mood'])
    
    # Create journal entry
    journal = Journal(
        user_id=user_id,
        content=data['content'],
        mood=data['mood'],
        emotion_positive=analysis['emotionScore']['positive'],
        emotion_neutral=analysis['emotionScore']['neutral'],
        emotion_negative=analysis['emotionScore']['negative'],
        wellness_score=analysis['wellnessScore']
    )
    
    try:
        db.session.add(journal)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'journal': journal.to_dict(),
            'analysis': analysis
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@journal_bp.route('/journal', methods=['GET'])
def get_journals():
    """Get all journals for current user"""
    user_id = request.args.get('user_id', type=int)
    timeframe = request.args.get('timeframe', 'all')
    
    if not user_id:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User authentication required'}), 401
        user_id = user.id
    
    # Base query
    query = Journal.query.filter_by(user_id=user_id)
    
    # Filter by timeframe
    if timeframe == 'week':
        week_ago = datetime.utcnow() - timedelta(days=7)
        query = query.filter(Journal.created_at >= week_ago)
    elif timeframe == 'month':
        month_ago = datetime.utcnow() - timedelta(days=30)
        query = query.filter(Journal.created_at >= month_ago)
    
    journals = query.order_by(Journal.created_at.desc()).all()
    
    return jsonify({
        'journals': [j.to_dict() for j in journals],
        'total': len(journals)
    })

@journal_bp.route('/journal/<int:journal_id>', methods=['GET'])
def get_journal(journal_id):
    """Get a specific journal entry"""
    journal = Journal.query.get_or_404(journal_id)
    return jsonify({'journal': journal.to_dict()})

@journal_bp.route('/journal/<int:journal_id>', methods=['PUT'])
def update_journal(journal_id):
    """Update a journal entry"""
    data = request.json
    journal = Journal.query.get_or_404(journal_id)
    
    # Update fields
    if 'content' in data:
        journal.content = data['content']
    if 'mood' in data:
        journal.mood = data['mood']
        # Re-analyze if mood changed
        analysis = AIService.analyze_emotion(journal.content, data['mood'])
        journal.emotion_positive = analysis['emotionScore']['positive']
        journal.emotion_neutral = analysis['emotionScore']['neutral']
        journal.emotion_negative = analysis['emotionScore']['negative']
        journal.wellness_score = analysis['wellnessScore']
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'journal': journal.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@journal_bp.route('/journal/<int:journal_id>', methods=['DELETE'])
def delete_journal(journal_id):
    """Delete a journal entry"""
    journal = Journal.query.get_or_404(journal_id)
    
    try:
        db.session.delete(journal)
        db.session.commit()
        return jsonify({'success': True, 'message': 'Journal deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@journal_bp.route('/journal/stats', methods=['GET'])
def get_journal_stats():
    """Get statistics for user's journals"""
    user_id = request.args.get('user_id', type=int)
    timeframe = request.args.get('timeframe', 'week')
    
    if not user_id:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'User authentication required'}), 401
        user_id = user.id
    
    # Base query
    query = Journal.query.filter_by(user_id=user_id)
    
    # Filter by timeframe
    if timeframe == 'week':
        week_ago = datetime.utcnow() - timedelta(days=7)
        query = query.filter(Journal.created_at >= week_ago)
    elif timeframe == 'month':
        month_ago = datetime.utcnow() - timedelta(days=30)
        query = query.filter(Journal.created_at >= month_ago)
    
    journals = query.all()
    
    if not journals:
        return jsonify({
            'total_entries': 0,
            'average_wellness': 0,
            'mood_distribution': {},
            'streak_days': 0,
            'emotion_trend': []
        })
    
    # Calculate stats
    total = len(journals)
    avg_wellness = sum(j.wellness_score or 0 for j in journals) / total
    
    mood_counts = {}
    for journal in journals:
        mood = journal.mood
        mood_counts[mood] = mood_counts.get(mood, 0) + 1
    
    # Calculate streak
    streak_days = calculate_streak(journals)
    
    # Emotion trend (last 7 entries)
    emotion_trend = [
        {
            'date': j.created_at.isoformat() if j.created_at else None,
            'wellness': j.wellness_score
        }
        for j in sorted(journals, key=lambda x: x.created_at, reverse=True)[:7]
    ]
    
    return jsonify({
        'total_entries': total,
        'average_wellness': round(avg_wellness, 1),
        'mood_distribution': mood_counts,
        'streak_days': streak_days,
        'emotion_trend': emotion_trend
    })

def calculate_streak(journals):
    """Calculate consecutive days with journal entries"""
    if not journals:
        return 0
    
    # Sort by date descending
    sorted_journals = sorted(journals, key=lambda x: x.created_at, reverse=True)
    
    streak = 0
    today = datetime.utcnow().date()
    
    for i, journal in enumerate(sorted_journals):
        journal_date = journal.created_at.date() if journal.created_at else None
        if not journal_date:
            continue
        
        expected_date = today - timedelta(days=i)
        if journal_date == expected_date:
            streak += 1
        else:
            break
    
    return streak
