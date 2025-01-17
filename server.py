
import socket
from _thread import *
from datetime import datetime
from client_class import Client 
from chat import Chat


HOST = '127.0.0.1'
PORT = 65421
THREAD_COUNT = 10
MESSAGE_SIZE = 1024

SAVE_FILE_PATH = "data.txt"


class Server:
    def __init__(self):
        self.__chat = Chat()
        self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__server.bind((HOST, PORT))
        self.__server.listen()

        print(f"Server is listening on port {PORT}")

    def client_handler(self, client):
        client.send_message('You are now connected to the server and can send messages.\n To send a user a message write it like user@@message:')

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
        now = datetime.now()
        datetime_string = now.strftime("%Y-%m-%d %H:%M:%S")
        message_data = f"(from : {client.name}, message: {message}, datetime: {datetime_string})\n"
        self.__chat.messages.append(message_data)
        self.save_data(message_data)

        data = message.split('@@')
        client_name = data[0]
        message = data[1] if len(data) > 1 else ""
        for c in self.__chat.clients:
            if(c.name == client_name and c.name != client.name):
                print(f"Sending message to {c.name}")
                c.send_message(f"[{client.name}]: {message}")

    def save_data(self, data):
        with open(SAVE_FILE_PATH, "a") as file:
            file.write(data)

    def close_server(self):
        print("Closing server")
        self.__server.close()



def main():
    server = Server()
    while True:
        server.accept_connection()

if __name__ == '__main__':
    main()
