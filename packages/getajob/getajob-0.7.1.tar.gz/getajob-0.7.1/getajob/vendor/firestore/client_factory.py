import json
import firebase_admin
from firebase_admin import credentials, firestore

from getajob.abstractions.vendor_client_factory import VendorClientFactory
from getajob.config.settings import SETTINGS

from .mock import MockFirestoreClient


class FirestoreClientFactory(VendorClientFactory):
    @staticmethod
    def _return_mock():
        return MockFirestoreClient()

    @staticmethod
    def _return_client():
        if len(firebase_admin._apps) == 0:
            cred = credentials.Certificate(json.loads(SETTINGS.FIRESTORE_JSON_CONFIG))
            firebase_admin.initialize_app(cred, name=SETTINGS.FIRESTORE_APP_NAME)
        return firestore.client(
            app=firebase_admin.get_app(name=SETTINGS.FIRESTORE_APP_NAME)
        )
