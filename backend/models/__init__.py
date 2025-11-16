from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .user import User, PrivacySettings
from .journal import Journal
from .message import DailyMessage

__all__ = ['db', 'User', 'PrivacySettings', 'Journal', 'DailyMessage']

