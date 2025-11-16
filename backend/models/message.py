from datetime import datetime
from . import db

class DailyMessage(db.Model):
    __tablename__ = 'daily_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), default='Breaking The Limits')
    display_date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(50), default='scheduled')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'message': self.message,
            'author': self.author,
            'display_date': self.display_date.isoformat() if self.display_date else None,
            'status': self.status,
            'date': self.display_date.isoformat() if self.display_date else None
        }
    
    def __repr__(self):
        return f'<DailyMessage {self.id}>'

