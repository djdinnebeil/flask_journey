from flask_login import UserMixin
from app.core import db

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False, nullable=False)
    banned_at = db.Column(db.DateTime, nullable=True, default=None)
    deleted_at = db.Column(db.DateTime, nullable=True, default=None)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'is_admin': self.is_admin,
            'banned_at': self.banned_at,
            'deleted_at': self.deleted_at
        }