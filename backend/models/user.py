from datetime import datetime

class User:
    def __init__(self, id, name, email, password_hash, role='student'):
        self.id = id
        self.name = name
        self.email = email
        self.password_hash = password_hash
        self.role = role  # 'student', 'parent', 'admin'
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }