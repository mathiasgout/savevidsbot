from app import logger
from db.firebase_db import get_document

from flask import current_app
from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, id: str) -> None:
        super().__init__()
        self.id = id
    
    def _get_auth_document(self):
        try:
            auth_document = get_document(collection_name=current_app.config["AUTH_COLLECTION"], document_name=self.id)
        except Exception as e:
            logger.error(f"Error occured : {e}")
            return None
        return auth_document
    
    def get_user(self):
        auth_document = self._get_auth_document()

        # Chargement de l'attributs "password"
        if auth_document:
            self.password = auth_document["password"]
            return self
        return None
