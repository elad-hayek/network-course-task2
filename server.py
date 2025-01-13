
# for server
import socket
from _thread import *
import json
import os

# for chat
import uuid 

HOST = '127.0.0.1'
PORT = 65421
THREAD_COUNT = 10
MESSAGE_SIZE = 1024

SAVE_FILE_PATH = "data.json"


class Server:
    def __init__(self):
        self.__chat = Chat()
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((HOST, PORT))
        self.__server.listen()

        print(f"Server is listening on port {PORT}")

    def client_handler(self, client):
        client.send_message('You are now connected to the server and can send messages:')

        while True:
            try:
                message = client.socket.recv(MESSAGE_SIZE).decode('utf-8')
                if message == 'CLOSE_CLIENT':
                    break

                self.handle_message(client, message)
            except socket.error as e:
                print(f"Error receiving message from {client.name}: {e}")
                break

        self.close_client(client) 

    def handle_message(self, client, message):
        if(message == 'CLOSE_CLIENT'):
            self.close_client(client)
        else:
            self.send_message_in_chat(client, message)


    def accept_connection(self):
        client_socket, client_address = self.__server.accept()
        print('Connected to: ' + client_address[0] + ':' + str(client_address[1]))
        client_name = client_socket.recv(MESSAGE_SIZE).decode()
        client = Client(client_name, client_address, client_socket)
        self.join_chat(client)
        start_new_thread(self.client_handler, (client,))


    def join_chat(self, client):
        self.__chat.add_client(client)

    def close_client(self, client):
        print(f"Closing connection to {client.name}")
        self.__chat.remove_client(client)
        client.socket.close()

    def send_message_in_chat(self, client, message):
        print(f"Sending message in chat {client.chat_id}")
        self.__chat.messages.append({"from": client.name, "message": message})
        self.save_data()

        data = message.split('@@')
        client_name = data[0]
        message = data[1] if len(data) > 1 else ""
        try:
            for c in self.__chat.clients:
                if(c.name == client_name and c.name != client.name):
                    print(f"Sending message to {c.name}")
                    c.send_message(f"[{client.name}]: {message}")
        except socket.error as e:
            print(f"Error sending message to {c.name}: {e}")

    def save_data(self):
        with open(SAVE_FILE_PATH, "w") as file:
            json.dump(self.__chat.messages, file, indent=4)


    def close_server(self):
        print("Closing server")
        self.save_data()

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
            response = self.socket.recv(MESSAGE_SIZE).decode('utf-8')
            print(response)

        except socket.error as e:
            print(f"Error connecting to server: {e}")


    def receive_message(self):
        try:
            data = self.socket.recv(MESSAGE_SIZE).decode('utf-8')
            print(data) 
            return data
        except socket.error as e:
            print(f"Error receiving message: {e}")

    def send_message(self, message):
        try:
            self.socket.send(message.encode())
        except socket.error as e:
            print(f"Error sending message: {e}") 

    def close(self):
        self.socket.close()
        print("Connection closed")


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


def main():
    server = Server()
    while True:
        server.accept_connection()

if __name__ == '__main__':
    main()
