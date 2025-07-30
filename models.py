import os
import uuid
import json
from datetime import datetime

DATA_DIR = os.path.join(os.path.dirname(__file__), 'data', 'pastes')

class Paste:
    def __init__(self, content, title=None, lang=None, url_id=None, created=None, expire_at=None, max_views=None, views=0, password=None, tags=None, author=None, theme=None, private=False, public=False):
        self.content = content
        self.title = title or ''
        self.lang = lang or ''
        self.url_id = url_id or self.generate_id()
        self.created = created or datetime.utcnow().isoformat()
        self.expire_at = expire_at
        self.max_views = max_views
        self.views = views
        self.password = password
        self.tags = tags or []
        self.author = author or ''
        self.theme = theme or 'light'
        self.private = private
        self.public = public

    @staticmethod
    def generate_id():
        return uuid.uuid4().hex[:8]

    @property
    def filepath(self):
        return os.path.join(DATA_DIR, f'{self.url_id}.json')

    def save(self):
        os.makedirs(DATA_DIR, exist_ok=True)
        with open(self.filepath, 'w', encoding='utf-8') as f:
            json.dump(self.__dict__, f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, url_id):
        path = os.path.join(DATA_DIR, f'{url_id}.json')
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        # Compatibilidad retro
        if 'private' not in data:
            data['private'] = False
        if 'public' not in data:
            data['public'] = False
        return cls(**data)
    @staticmethod
    def list_all():
        """Devuelve todos los pastes ordenados por fecha descendente."""
        files = [f for f in os.listdir(DATA_DIR) if f.endswith('.json')]
        pastes = []
        for f in files:
            try:
                with open(os.path.join(DATA_DIR, f), 'r', encoding='utf-8') as fp:
                    data = json.load(fp)
                p = Paste(**data)
                pastes.append(p)
            except Exception:
                continue
        return sorted(pastes, key=lambda p: p.created, reverse=True)
