import socket

# Define the maximum size of messages that can be sent/received
MESSAGE_SIZE = 1024

class Client:
    def __init__(self, name, address="", client_socket=None):
        """
        Initialize a Client instance.
        
        Args:
            name (str): The name of the client.
            address (str): The address of the client (default is empty).
            client_socket (socket): Optional pre-existing socket for the client.
        """
        self.name = name
        self.address = address
        self.chat_id = None  # To be assigned when the client joins a chat

        # Use the provided socket or create a new one
        if client_socket:
            self.socket = client_socket
        else:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self, server_ip, server_port):
        """
        Connect to a server using the provided IP address and port.

        Args:
            server_ip (str): The IP address of the server.
            server_port (int): The port number of the server.

        Prints a success message upon connection or an error message if the connection fails.
        """
        print(f"Connecting to server {server_ip}:{server_port}")
        try:
            # Attempt to connect to the server
            self.socket.connect((server_ip, server_port))
            # Send the client's name to the server
            self.socket.sendall(self.name.encode())
            # Receive and print the server's response
            response = self.socket.recv(MESSAGE_SIZE).decode('utf-8')
            print(response)

        except socket.error as e:
            # Handle connection errors
            print(f"Error connecting to server: {e}")

    def receive_message(self):
        """
        Receive a message from the server.

        Returns:
            str: The received message decoded as a string.

        Prints the received message to the console.
        """
        data = self.socket.recv(MESSAGE_SIZE).decode('utf-8')
        print(data) 
        return data

    def send_message(self, message):
        """
        Send a message to the server.

        Args:
            message (str): The message to send.

        Prints an error message if sending fails.
        """
        try:
            self.socket.send(message.encode())
        except socket.error as e:
            # Handle errors during message sending
            print(f"Error sending message: {e}") 

    def close(self):
        """
        Close the client socket connection.

        Prints a confirmation message when the connection is closed.
        """
        self.socket.close()
        print("Connection closed")

