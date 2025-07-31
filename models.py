from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), unique=True, nullable=False)
    title = db.Column(db.String(128))
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(32))
    author = db.Column(db.String(64))
    tags = db.Column(db.String(128))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime)
    max_views = db.Column(db.Integer)
    views = db.Column(db.Integer, default=0)
    password_hash = db.Column(db.String(128))
    edit_code = db.Column(db.String(64))
    is_private = db.Column(db.Boolean, default=False)
    one_time = db.Column(db.Boolean, default=False)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
