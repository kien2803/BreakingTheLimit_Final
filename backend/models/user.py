from datetime import datetime
from . import db
import hashlib
import secrets

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='student')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    
    # Relationships
    journals = db.relationship('Journal', backref='user', lazy=True, cascade='all, delete-orphan')
    privacy_settings = db.relationship('PrivacySettings', backref='user', uselist=False, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set password using SHA256 (simplified for development)"""
        # In production, use bcrypt
        salt = secrets.token_hex(16)
        hash_obj = hashlib.sha256((password + salt).encode('utf-8'))
        self.password_hash = f"{salt}:{hash_obj.hexdigest()}"
    
    def check_password(self, password):
        """Check if password matches"""
        try:
            salt, stored_hash = self.password_hash.split(':')
            hash_obj = hashlib.sha256((password + salt).encode('utf-8'))
            return hash_obj.hexdigest() == stored_hash
        except:
            # Fallback for old bcrypt hashes if any
            return False
    
    def to_dict(self, include_sensitive=False):
        """Convert to dictionary"""
        data = {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'is_active': self.is_active
        }
        if include_sensitive:
            data['updated_at'] = self.updated_at.isoformat() if self.updated_at else None
        return data
    
    def __repr__(self):
        return f'<User {self.email}>'

class PrivacySettings(db.Model):
    __tablename__ = 'privacy_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    share_emotions = db.Column(db.Boolean, default=True)
    alert_parents = db.Column(db.Boolean, default=True)
    receive_messages = db.Column(db.Boolean, default=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        return {
            'share_emotions': self.share_emotions,
            'alert_parents': self.alert_parents,
            'receive_messages': self.receive_messages
        }
