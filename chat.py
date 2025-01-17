
import uuid 

class Chat:
    def __init__(self):
        self.messages = []
        self.id = str(uuid.uuid4())
        self.clients = []

    def add_client(self, client):
        client.chat_id = self.id
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)
