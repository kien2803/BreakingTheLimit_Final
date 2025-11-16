from datetime import datetime
from . import db

class Journal(db.Model):
    __tablename__ = 'journals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    mood = db.Column(db.String(50), nullable=False)
    emotion_positive = db.Column(db.Float)
    emotion_neutral = db.Column(db.Float)
    emotion_negative = db.Column(db.Float)
    wellness_score = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'mood': self.mood,
            'emotion_score': {
                'positive': self.emotion_positive,
                'neutral': self.emotion_neutral,
                'negative': self.emotion_negative
            },
            'wellness_score': self.wellness_score,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Journal {self.id}>'
