from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import db, User, Journal, PrivacySettings
from sqlalchemy import and_, func, text
from routes.auth import get_current_user

family_bp = Blueprint('family', __name__)

@family_bp.route('/link', methods=['POST'])
def link_family():
    """Create a family connection request"""
    data = request.json
    
    parent_id = data.get('parent_id')
    child_email = data.get('child_email')
    
    if not parent_id or not child_email:
        return jsonify({'error': 'Parent ID and child email are required'}), 400
    
    # Find child by email
    child = User.query.filter_by(email=child_email, role='student').first()
    if not child:
        return jsonify({'error': 'Student not found'}), 404
    
    # Check if connection already exists
    existing = db.session.execute(
        text("SELECT * FROM family_connections WHERE parent_id=:pid AND child_id=:cid"),
        {'pid': parent_id, 'cid': child.id}
    ).fetchone()
    
    if existing:
        return jsonify({'error': 'Connection already exists'}), 400
    
    # Create connection (using raw SQL for now)
    db.session.execute(
        text("""
            INSERT INTO family_connections (parent_id, child_id, relationship, status)
            VALUES (:pid, :cid, :rel, 'pending')
        """),
        {'pid': parent_id, 'cid': child.id, 'rel': data.get('relationship', 'parent')}
    )
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Connection request sent'
    }), 201

@family_bp.route('/children', methods=['GET'])
def get_children():
    """Get all children connected to a parent"""
    parent_id = request.args.get('parent_id', type=int)
    
    if not parent_id:
        user = get_current_user()
        if not user or user.role != 'parent':
            return jsonify({'error': 'Parent authentication required'}), 401
        parent_id = user.id
    
    # Get connected children
    connections = db.session.execute(
        text("""
            SELECT c.id, c.name, c.email, c.last_login, fc.relationship
            FROM family_connections fc
            JOIN users c ON fc.child_id = c.id
            WHERE fc.parent_id = :pid AND fc.status = 'accepted'
        """),
        {'pid': parent_id}
    ).fetchall()
    
    children = []
    for conn in connections:
        child_id, name, email, last_login, relationship = conn
        
        # Get latest journal for wellness score
        latest_journal = Journal.query.filter_by(user_id=child_id)\
            .order_by(Journal.created_at.desc()).first()
        
        wellness_score = latest_journal.wellness_score if latest_journal else None
        recent_mood = latest_journal.mood if latest_journal else None
        
        children.append({
            'id': child_id,
            'name': name,
            'email': email,
            'lastActive': last_login.isoformat() if last_login else None,
            'wellnessScore': wellness_score,
            'recentMood': recent_mood,
            'relationship': relationship
        })
    
    return jsonify({'children': children})

@family_bp.route('/child/<int:child_id>/summary', methods=['GET'])
def get_child_summary(child_id):
    """Get emotion summary for a specific child"""
    timeframe = request.args.get('timeframe', 'week')
    
    # Calculate date range
    if timeframe == 'week':
        start_date = datetime.utcnow() - timedelta(days=7)
    elif timeframe == 'month':
        start_date = datetime.utcnow() - timedelta(days=30)
    else:
        start_date = datetime.utcnow() - timedelta(days=90)
    
    # Get journals in timeframe
    journals = Journal.query.filter(
        and_(
            Journal.user_id == child_id,
            Journal.created_at >= start_date
        )
    ).order_by(Journal.created_at.asc()).all()
    
    if not journals:
        return jsonify({
            'child_id': child_id,
            'timeframe': timeframe,
            'wellness_score': None,
            'trend': '0',
            'journal_count': 0,
            'streak_days': 0,
            'mood_variation': 'No data',
            'emotion_data': {'positive': [], 'neutral': [], 'negative': []},
            'alerts': []
        })
    
    # Calculate averages
    avg_wellness = sum(j.wellness_score or 0 for j in journals) / len(journals)
    latest_wellness = journals[-1].wellness_score if journals else None
    
    # Calculate trend
    if len(journals) >= 7:
        week_ago_avg = sum(j.wellness_score or 0 for j in journals[:7]) / 7
        trend = f"+{int(avg_wellness - week_ago_avg)}" if avg_wellness > week_ago_avg else f"{int(avg_wellness - week_ago_avg)}"
    else:
        trend = "0"
    
    # Get emotion data for chart (last 7 days)
    recent_journals = journals[-7:] if len(journals) >= 7 else journals
    emotion_data = {
        'positive': [j.emotion_positive or 0 for j in recent_journals],
        'neutral': [j.emotion_neutral or 0 for j in recent_journals],
        'negative': [j.emotion_negative or 0 for j in recent_journals]
    }
    
    # Calculate streak
    streak_days = calculate_streak(journals)
    
    # Generate alerts
    alerts = []
    if avg_wellness < 50:
        alerts.append({
            'type': 'warning',
            'message': 'Điểm bình an thấp, cần quan tâm đặc biệt'
        })
    elif latest_wellness and latest_wellness < 40:
        alerts.append({
            'type': 'critical',
            'message': 'Cảnh báo: Điểm bình an rất thấp, cần can thiệp ngay'
        })
    
    return jsonify({
        'child_id': child_id,
        'timeframe': timeframe,
        'wellness_score': int(avg_wellness),
        'trend': trend,
        'journal_count': len(journals),
        'streak_days': streak_days,
        'mood_variation': 'Ổn định' if len(set(j.mood for j in journals)) <= 3 else 'Biến động',
        'emotion_data': emotion_data,
        'alerts': alerts
    })

def calculate_streak(journals):
    """Calculate consecutive days with journal entries"""
    if not journals:
        return 0
    
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

@family_bp.route('/encourage', methods=['POST'])
def send_encouragement():
    """Send encouragement message from parent to child"""
    data = request.json
    
    parent_id = data.get('parent_id')
    child_id = data.get('child_id')
    message_text = data.get('message')
    
    if not all([parent_id, child_id, message_text]):
        return jsonify({'error': 'Parent ID, child ID, and message are required'}), 400
    
    db.session.execute(
        text("""
            INSERT INTO encouragement_messages (parent_id, child_id, message, is_read)
            VALUES (:pid, :cid, :msg, 0)
        """),
        {'pid': parent_id, 'cid': child_id, 'msg': message_text}
    )
    db.session.commit()
    
    return jsonify({
        'success': True,
        'message': 'Encouragement sent'
    })

@family_bp.route('/privacy', methods=['PUT'])
def update_privacy():
    """Update student privacy settings"""
    user_id = request.json.get('user_id')
    
    if not user_id:
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        user_id = user.id
    
    privacy = PrivacySettings.query.filter_by(user_id=user_id).first()
    if not privacy:
        privacy = PrivacySettings(user_id=user_id)
        db.session.add(privacy)
    
    data = request.json
    if 'share_emotions' in data:
        privacy.share_emotions = data['share_emotions']
    if 'alert_parents' in data:
        privacy.alert_parents = data['alert_parents']
    if 'receive_messages' in data:
        privacy.receive_messages = data['receive_messages']
    
    try:
        db.session.commit()
        return jsonify({
            'success': True,
            'settings': privacy.to_dict()
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500
