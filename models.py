# models.py - Modelo de datos principal para PartyBin
import os
import json
from datetime import datetime
from typing import List, Optional

PASTES_DIR = os.path.join(os.path.dirname(__file__), 'data', 'pastes')

class Paste:
    def __init__(self, id: str, content: str, title: str = '', author: str = '',
                 created_at: Optional[str] = None, updated_at: Optional[str] = None,
                 language: str = '', tags: Optional[List[str]] = None,
                 max_views: Optional[int] = None, views: int = 0,
                 expire_at: Optional[str] = None, password: Optional[str] = None,
                 edit_code: Optional[str] = None, private: bool = False):
        self.id = id
        self.content = content
        self.title = title
        self.author = author
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.updated_at = updated_at or self.created_at
        self.language = language
        self.tags = tags or []
        self.max_views = max_views
        self.views = views
        self.expire_at = expire_at
        self.password = password
        self.edit_code = edit_code
        self.private = private

    def to_dict(self):
        return self.__dict__

    def save(self):
        path = os.path.join(PASTES_DIR, f'{self.id}.json')
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @staticmethod
    def load(paste_id: str):
        path = os.path.join(PASTES_DIR, f'{paste_id}.json')
        if not os.path.exists(path):
            return None
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return Paste(**data)

    @staticmethod
    def all():
        pastes = []
        for fname in os.listdir(PASTES_DIR):
            if fname.endswith('.json'):
                with open(os.path.join(PASTES_DIR, fname), 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    pastes.append(Paste(**data))
        return pastes
