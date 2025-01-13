
# for server
import socket
from _thread import *

# for chat
import uuid 

HOST = '127.0.0.1'
PORT = 65421
THREAD_COUNT = 5
MESSAGE_SIZE = 1024



class Server:
    def __init__(self):
        self.__clients = {}
        self.__chats = {}
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((HOST, PORT))
        self.__server.listen()
        print(f"Server is listening on port {PORT}")

    def client_handler(self, client):
        client.socket.send(str.encode('You are now connected to the server'))
        while True:
            try:
                print(f"Waiting for message from {client.name}")
                data = client.socket.recv(MESSAGE_SIZE)
                message = data.decode('utf-8')
                if message == 'CLOSE_CLIENT':
                    break

                self.handle_message(client, message)
            except socket.error as e:
                print(f"Error receiving message from {client.name}: {e}")
                break

        self.close_client(client) 

    def handle_message(self, client, message):
        print(f"Received message from {client.name}: {message}")
        message = message.split('&&') 
        command = message[0]
        arg = message[1] if len(message) > 1 else None

        if(arg is not None and arg == 'chat_mode'):
            self.send_message_in_chat(client, command)
            return

        if(command == 'CREATE_CHAT'):
            self.create_chat(client)
        elif(command == 'JOIN_CHAT'):
            self.join_chat(client, arg)
        elif(command == 'EXIT_CHAT'):
            self.exit_chat(client)
        else:
            self.send_message_in_chat(client, command)


    def accept_connection(self):
        client_socket, client_address = self.__server.accept()
        print('Connected to: ' + client_address[0] + ':' + str(client_address[1]))
        client_name = client_socket.recv(MESSAGE_SIZE).decode()
        client = Client(client_name, client_address, client_socket)
        self.__clients[client.name] = client
        start_new_thread(self.client_handler, (client,))

    def create_chat(self, client):
        chat = Chat()
        chat.add_client(client)
        self.__chats[chat.id] = chat
        client.chat_id = chat.id
        client.send_message(f"Chat created with id {chat.id}, you can now send messages:")

    def join_chat(self, client, chat_id):
        chat = self.__chats.get(chat_id)
        if(chat is None):
            client.send_message("Chat does not exist")
            return

        chat.add_client(client)
        client.chat_id = chat_id
        client.send_message(f"Joined chat {chat_id}, you can now send messages:")

    def exit_chat(self, client):
        chat = self.__chats[client.chat_id]
        chat.remove_client(client)
        client.chat_id = None
        client.send_message("Exited chat")

        if len(chat.clients) == 0:
            del self.__chats[chat.id]

    def close_client(self, client):
        print(f"Closing connection to {client.name}")
        client.socket.close()

    def send_message_in_chat(self, client, message):
        print(f"Sending message in chat {client.chat_id}")
        chat = self.__chats[client.chat_id]
        for c in chat.clients:
            try:
                if(c.name != client.name):
                    print(f"Sending message to {c.name}")
                    c.send_message(f"[{client.name}]: {message}")
            except socket.error as e:
                print(f"Error sending message to {c.name}: {e}")


    def close_server(self):
        print("Closing server")
        # TODO: save chats to file

        self.__server.close()


MESSAGE_SIZE = 1024

class Client:
    def __init__(self, name, address = "", client_socket = None):
        self.name = name
        self.address = address
        self.chat_id = None

        if(client_socket):
            self.socket = client_socket
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, server_ip, server_port):
        print(f"Connecting to server {server_ip}:{server_port}")
        try:
            self.socket.connect((server_ip, server_port))
            self.socket.sendall(self.name.encode())
            response = self.socket.recv(MESSAGE_SIZE).decode()
            self.handle_response(response)

        except socket.error as e:
            print(f"Error connecting to server: {e}")


    def send_message_and_await_response(self, data):
        self.send_message(data)
        start_new_thread(self.receive_message, ())
        
    def receive_message(self):
        try:
            data = self.socket.recv(MESSAGE_SIZE).decode('utf-8')
            self.handle_response(data)
            return data
        except socket.error as e:
            print(f"Error receiving message: {e}")

    def send_message(self, message):
        try:
            self.socket.send(message.encode())
        except socket.error as e:
            print(f"Error sending message: {e}") 

    def handle_response(self, response):
        print(response)

    def close(self):
        self.socket.close()
        print("Connection closed")


class Message:
    def __init__(self, message):
        # self.client_name = client_name
        self.message = message
        # self.chat_id = chat_id

    def create_message(self):
        return f"{self.message}"



class Chat:
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.clients = []

    def add_client(self, client):
        self.clients.append(client)

    def remove_client(self, client):
        self.clients.remove(client)



def main():
    server = Server()
    while True:
        server.accept_connection()

if __name__ == '__main__':
    main()
