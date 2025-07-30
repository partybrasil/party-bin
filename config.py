import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'partybin-secret')
    # Configuración de temas y otras opciones globales
    THEMES = [
        'light', 'dark', 'hacker', 'monokai', 'dracula', 'solarized',
        'nord', 'gruvbox', 'pastel', 'party', 'classic'
    ]
    DEFAULT_THEME = 'light'

class DevConfig(Config):
    DEBUG = True

class ProdConfig(Config):
    DEBUG = False
