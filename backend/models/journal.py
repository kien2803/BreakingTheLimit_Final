from datetime import datetime

class Journal:
    def __init__(self, id, user_id, content, mood):
        self.id = id
        self.user_id = user_id
        self.content = content
        self.mood = mood
        self.emotion_score = None
        self.wellness_score = None
        self.created_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'content': self.content,
            'mood': self.mood,
            'emotion_score': self.emotion_score,
            'wellness_score': self.wellness_score,
            'created_at': self.created_at.isoformat()
        }