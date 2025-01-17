import socket


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
        data = self.socket.recv(MESSAGE_SIZE).decode('utf-8')
        print(data) 
        return data

    def send_message(self, message):
        try:
            self.socket.send(message.encode())
        except socket.error as e:
            print(f"Error sending message: {e}") 

    def close(self):
        self.socket.close()
        print("Connection closed")


