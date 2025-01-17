import socket
from _thread import *
from datetime import datetime
from client_class import Client 
from chat import Chat

# Constants for server configuration
HOST = '127.0.0.1'  
PORT = 65421  
THREAD_COUNT = 10  
MESSAGE_SIZE = 1024  
SAVE_FILE_PATH = "data.txt"  

class Server:
    def __init__(self):
        """
        Initializes the server.
        - Creates a Chat instance to manage clients and messages.
        - Sets up the server socket to listen for incoming connections.
        """
        self.__chat = Chat()
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((HOST, PORT))
        self.__server.listen()

        print(f"Server is listening on port {PORT}")

    def client_handler(self, client):
        """
        Handles communication with a connected client.
        - Sends an initial message to the client.
        - Continuously listens for messages from the client.
        - Handles client disconnection.
        """
        client.send_message('You are now connected to the server and can send messages.\n To send a user a message write it like user@@message:')

        while True:
            try:
                # Receive and decode the message from the client
                message = client.socket.recv(MESSAGE_SIZE).decode('utf-8')
                if message == 'CLOSE_CLIENT':
                    break

                # Process the received message
                self.handle_message(client, message)
            except socket.error as e:
                print(f"Error receiving message from {client.name}: {e}")
                break

        # Close the client connection when done
        self.close_client(client)

    def handle_message(self, client, message):
        """
        Processes a message received from a client.
        - Handles special cases like client disconnection.
        - Sends messages in the chat.
        """
        if message == 'CLOSE_CLIENT':
            self.close_client(client)
        else:
            self.send_message_in_chat(client, message)

    def accept_connection(self):
        """
        Accepts an incoming client connection.
        - Receives the client's name.
        - Adds the client to the chat.
        - Starts a new thread to handle the client's communication.
        """
        client_socket, client_address = self.__server.accept()
        print('Connected to: ' + client_address[0] + ':' + str(client_address[1]))
        client_name = client_socket.recv(MESSAGE_SIZE).decode()
        client = Client(client_name, client_address, client_socket)
        self.join_chat(client)
        start_new_thread(self.client_handler, (client,))

    def join_chat(self, client):
        """
        Adds a client to the chat.
        """
        self.__chat.add_client(client)

    def close_client(self, client):
        """
        Closes the connection with a client.
        - Removes the client from the chat.
        - Closes the client socket.
        """
        print(f"Closing connection to {client.name}")
        self.__chat.remove_client(client)
        client.socket.close()

    def send_message_in_chat(self, client, message):
        """
        Sends a message in the chat.
        - Formats the message with metadata (sender, message content, timestamp).
        - Appends the message to the chat history.
        - Sends the message to the target client if specified.
        """
        print(f"Sending message in chat {client.chat_id}")
        now = datetime.now()
        datetime_string = now.strftime("%Y-%m-%d %H:%M:%S")
        message_data = f"(from : {client.name}, message: {message}, datetime: {datetime_string})\n"
        self.__chat.messages.append(message_data)
        self.save_data(message_data)

        # Parse the message to check for a target client
        data = message.split('@@')
        client_name = data[0]
        message = data[1] if len(data) > 1 else ""
        for c in self.__chat.clients:
            if c.name == client_name and c.name != client.name:
                print(f"Sending message to {c.name}")
                c.send_message(f"[{client.name}]: {message}")

    def save_data(self, data):
        """
        Saves chat data to a file.
        - Appends the message to a text file.
        """
        with open(SAVE_FILE_PATH, "a") as file:
            file.write(data)

    def close_server(self):
        """
        Closes the server socket.
        """
        print("Closing server")
        self.__server.close()


def main():
    """
    Main function to start the server.
    - Continuously accepts incoming client connections.
    """
    server = Server()
    while True:
        server.accept_connection()


if __name__ == '__main__':
    main()
