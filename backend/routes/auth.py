from flask import Blueprint, request, jsonify
from datetime import datetime
from models import db, User, PrivacySettings
from functools import wraps

auth_bp = Blueprint('auth', __name__)

def get_current_user():
    """Get current user from token (simplified for now)"""
    # In production, decode JWT token here
    user_id = request.headers.get('X-User-ID')
    if user_id:
        return User.query.get(int(user_id))
    return None

def require_auth(f):
    """Decorator to require authentication"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = get_current_user()
        if not user:
            return jsonify({'error': 'Authentication required'}), 401
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.json
    
    # Validate input
    if not data.get('name') or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Name, email, and password are required'}), 400
    
    # Check if user exists
    existing_user = User.query.filter_by(email=data['email']).first()
    if existing_user:
        return jsonify({'error': 'Email already registered'}), 400
    
    # Create new user
    user = User(
        name=data['name'],
        email=data['email'],
        role=data.get('role', 'student')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Create default privacy settings
        privacy = PrivacySettings(user_id=user.id)
        db.session.add(privacy)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'user': user.to_dict(),
            'message': 'Registration successful'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/auth/login', methods=['POST'])
def login():
    """Login user"""
    data = request.json
    
    if not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Email and password are required'}), 400
    
    # Find user
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401
    
    if not user.is_active:
        return jsonify({'error': 'Account is deactivated'}), 403
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Generate token (simplified - in production use JWT)
    token = f"token_{user.id}_{datetime.utcnow().timestamp()}"
    
    return jsonify({
        'success': True,
        'token': token,
        'user': user.to_dict(),
        'message': 'Login successful'
    })

@auth_bp.route('/auth/me', methods=['GET'])
@require_auth
def get_current_user_info():
    """Get current user information"""
    user = get_current_user()
    return jsonify({'user': user.to_dict()})

@auth_bp.route('/auth/logout', methods=['POST'])
@require_auth
def logout():
    """Logout user"""
    return jsonify({'success': True, 'message': 'Logged out successfully'})

@auth_bp.route('/auth/change-password', methods=['POST'])
@require_auth
def change_password():
    """Change user password"""
    data = request.json
    user = get_current_user()
    
    if not data.get('old_password') or not data.get('new_password'):
        return jsonify({'error': 'Old and new passwords are required'}), 400
    
    if not user.check_password(data['old_password']):
        return jsonify({'error': 'Current password is incorrect'}), 401
    
    user.set_password(data['new_password'])
    user.updated_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Password changed successfully'})

