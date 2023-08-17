from google.cloud import firestore
from google.oauth2 import service_account
import os
import threading
import warnings

warnings.filterwarnings("ignore", category=UserWarning)

class ApiSeiketsu:
    def __init__(self, token):
        self.db = self._get_firestore_client()
        self.new_message_event = threading.Event()
        self.token = token
        self.messages_ref = self.db.collection('messages')

        token_collection_ref = self.db.collection('bot_token')
        query = token_collection_ref.where(field_path='value', op_string='==', value=self.token)
        docs = query.limit(1).stream()

        if len(list(docs)) == 0:
            raise ValueError('Invalid token.')

        self._listen_for_changes()

    def _get_firestore_client(self):
        credentials_file = os.path.join(os.path.dirname(__file__), 'data', 'firebase_credentials.json')
        credentials = service_account.Credentials.from_service_account_file(credentials_file)
        return firestore.Client(credentials=credentials, project=credentials.project_id)

    def _listen_for_changes(self):
        query = self.messages_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
        query_watch = query.on_snapshot(self._on_snapshot)

    def _on_snapshot(self, col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                latest_message = change.document.to_dict()
                alias = latest_message['alias']
                message_text = latest_message['text']
                self.new_message_event.set()

    def read_message(self):
        while True:
            self.new_message_event.wait()

            query = self.messages_ref.order_by('timestamp', direction=firestore.Query.DESCENDING).limit(1)
            message_docs = query.stream()

            for message_doc in message_docs:
                latest_message = message_doc.to_dict()
                alias = latest_message['alias']
                message_text = latest_message['text']
                self.new_message_event.clear()
                return alias, message_text

    def write_message(self, alias, message_text):
        doc_ref = self.messages_ref.document()
        batch = self.db.batch()
        batch.set(doc_ref, {
            'alias': alias + '#BOT',
            'text': message_text,
            'timestamp': firestore.SERVER_TIMESTAMP
        })
        batch.commit()
