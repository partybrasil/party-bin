import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'partybin-secret-key')
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', f"sqlite:///{os.path.join(BASEDIR, 'data', 'party-bin.db')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_TYPE = 'filesystem'
    WTF_CSRF_ENABLED = True
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024  # 2MB por paste
    # Puedes agregar más configuraciones aquí
