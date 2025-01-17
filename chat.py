import uuid 

class Chat:
    def __init__(self):
        """
        Initializes a Chat instance.
        - Creates a unique ID for the chat.
        - Initializes an empty list for messages.
        - Initializes an empty list for connected clients.
        """
        self.messages = []
        self.id = str(uuid.uuid4())  # Unique identifier for the chat
        self.clients = []

    def add_client(self, client):
        """
        Adds a client to the chat.
        - Associates the chat's unique ID with the client.
        - Appends the client to the list of connected clients.
        """
        client.chat_id = self.id
        self.clients.append(client)

    def remove_client(self, client):
        """
        Removes a client from the chat.
        - Removes the client instance from the list of connected clients.
        """
        self.clients.remove(client)
