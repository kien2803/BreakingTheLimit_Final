from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import db, User, Journal, DailyMessage
from sqlalchemy import func, and_
from routes.auth import get_current_user, require_auth

admin_bp = Blueprint('admin', __name__)

def require_admin(f):
    """Decorator to require admin role"""
    from functools import wraps
    @wraps(f)
    @require_auth
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user or user.role != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/users', methods=['GET'])
@require_admin
def get_users():
    """Get all users"""
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 20, type=int)
    role = request.args.get('role')
    search = request.args.get('search')
    
    query = User.query
    
    if role:
        query = query.filter_by(role=role)
    if search:
        query = query.filter(
            (User.name.contains(search)) | (User.email.contains(search))
        )
    
    users = query.paginate(page=page, per_page=per_page, error_out=False)
    
    return jsonify({
        'users': [u.to_dict() for u in users.items],
        'total': users.total,
        'page': page,
        'per_page': per_page
    })

@admin_bp.route('/users/<int:user_id>', methods=['GET'])
@require_admin
def get_user(user_id):
    """Get specific user"""
    user = User.query.get_or_404(user_id)
    return jsonify({'user': user.to_dict(include_sensitive=True)})

@admin_bp.route('/users/<int:user_id>', methods=['PUT'])
@require_admin
def update_user(user_id):
    """Update user"""
    user = User.query.get_or_404(user_id)
    data = request.json
    
    if 'name' in data:
        user.name = data['name']
    if 'email' in data:
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    try:
        db.session.commit()
        return jsonify({'success': True, 'user': user.to_dict()})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/users/<int:user_id>', methods=['DELETE'])
@require_admin
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)
    
    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'success': True, 'message': 'User deleted'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/messages', methods=['GET'])
@require_admin
def get_messages():
    """Get all daily messages"""
    messages = DailyMessage.query.order_by(DailyMessage.display_date.desc()).all()
    return jsonify({'messages': [m.to_dict() for m in messages]})

@admin_bp.route('/messages', methods=['POST'])
@require_admin
def create_message():
    """Create daily message"""
    data = request.json
    
    message = DailyMessage(
        message=data['message'],
        author=data.get('author', 'Breaking The Limits'),
        display_date=datetime.strptime(data['display_date'], '%Y-%m-%d').date(),
        status=data.get('status', 'scheduled')
    )
    
    try:
        db.session.add(message)
        db.session.commit()
        return jsonify({'success': True, 'message': message.to_dict()}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@admin_bp.route('/stats', methods=['GET'])
@require_admin
def get_stats():
    """Get system statistics"""
    total_users = User.query.count()
    total_students = User.query.filter_by(role='student').count()
    total_parents = User.query.filter_by(role='parent').count()
    total_journals = Journal.query.count()
    
    # Today's journals
    today = datetime.utcnow().date()
    today_journals = Journal.query.filter(
        func.date(Journal.created_at) == today
    ).count()
    
    # Average wellness
    avg_wellness = db.session.query(func.avg(Journal.wellness_score)).scalar() or 0
    
    return jsonify({
        'total_users': total_users,
        'total_students': total_students,
        'total_parents': total_parents,
        'total_journals': total_journals,
        'today_journals': today_journals,
        'average_wellness': round(avg_wellness, 1)
    })

