# models.py - Modelos principales para PartyBin
import os
import json
import hashlib
import time
from datetime import datetime, timedelta
from slugify import slugify

DATA_PATH = os.path.join(os.path.dirname(__file__), 'data', 'pastes')

class Paste:
    def __init__(self, content, format='markdown', url=None, password=None, author=None, tags=None,
                 expiration=None, autodestruct=None, autodestruct_value=None, max_views=None, one_time=False,
                 title=None, created_at=None, last_viewed=None, views=0, edit_code=None, metadata=None):
        self.content = content
        self.format = format
        self.url = url or self.generate_url()
        self.password = password
        self.author = author
        self.tags = tags or []
        self.expiration = expiration
        self.autodestruct = autodestruct
        self.autodestruct_value = autodestruct_value
        self.max_views = max_views
        self.one_time = one_time
        self.title = title
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.last_viewed = last_viewed
        self.views = views
        self.edit_code = edit_code or self.generate_edit_code()
        self.metadata = metadata or {}

    def generate_url(self):
        # Genera una URL corta y única
        base = slugify(self.title) if self.title else ''
        rand = hashlib.sha1(str(time.time()).encode()).hexdigest()[:6]
        return base + '-' + rand if base else rand

    def generate_edit_code(self):
        # Genera un código de edición único
        return hashlib.sha256((self.url + str(time.time())).encode()).hexdigest()[:10]

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(data):
        return Paste(**data)

    def save(self):
        # Guarda el paste como JSON en data/pastes/<url>.json
        path = os.path.join(DATA_PATH, f'{self.url}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(url):
        path = os.path.join(DATA_PATH, f'{url}.json')
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Paste.from_dict(data)

    @staticmethod
    def delete(url):
        path = os.path.join(DATA_PATH, f'{url}.json')
        if os.path.exists(path):
            os.remove(path)

    @staticmethod
    def list_all():
        # Lista todos los pastes disponibles
        files = [f for f in os.listdir(DATA_PATH) if f.endswith('.json')]
        pastes = []
        for file in files:
            with open(os.path.join(DATA_PATH, file), 'r', encoding='utf-8') as f:
                data = json.load(f)
                pastes.append(Paste.from_dict(data))
        return pastes
