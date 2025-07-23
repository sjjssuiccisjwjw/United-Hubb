from app import db
from datetime import datetime

class PrivateKey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(20), unique=True, nullable=False)
    user_id = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    def __repr__(self):
        return f'<PrivateKey {self.key}>'
    
    def is_expired(self):
        return datetime.utcnow() > self.expires_at
