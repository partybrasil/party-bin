from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

class Paste(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(32), unique=True, nullable=False)
    title = db.Column(db.String(128))
    content = db.Column(db.Text, nullable=False)
    language = db.Column(db.String(32))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    max_views = db.Column(db.Integer, nullable=True)
    views = db.Column(db.Integer, default=0)
    one_time = db.Column(db.Boolean, default=False)
    edit_code = db.Column(db.String(128), nullable=True)
    password_hash = db.Column(db.String(128), nullable=True)
    is_private = db.Column(db.Boolean, default=False)
    tags = db.Column(db.String(128), nullable=True)
    author = db.Column(db.String(64), nullable=True)
    last_viewed = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
