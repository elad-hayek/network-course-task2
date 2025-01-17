from client_class import Client 
from _thread import *
import time

# Global variable to control receiving messages
stop_recive = False

def recive_messages(client):
    """
    Function to continuously receive messages from the server.
    - Runs in a separate thread.
    - Stops when the global variable `stop_recive` is set to True.
    """
    global stop_recive
    while not stop_recive:
        try:
            # Receive and process messages from the server
            client.receive_message()
        except Exception:
            # Stop receiving messages if an error occurs (e.g., server disconnects)
            stop_recive = True

def main():
    """
    Main function to start the client.
    - Prompts the user for their name.
    - Connects to the server.
    - Handles sending and receiving messages.
    """
    # Get the user's name and initialize the client
    name = input("Enter your name: ")
    client = Client(name)
    client.connect_to_server('127.0.0.1', 65421)

    global stop_recive
    while not stop_recive:
        # Start a new thread to receive messages from the server
        start_new_thread(recive_messages, (client,))

        # Prompt the user to enter a message
        message = input()

        if stop_recive:
            # Inform the user if the server is unavailable
            print(f"Sorry, {client.name} The server is not available!")
            client.close()
            break

        if message == 'exit':
            # Handle user exit by setting the stop flag and notifying the server
            stop_recive = True
            client.send_message("CLOSE_CLIENT")
            time.sleep(0.5)  # Give time for the message to be sent
            client.close()
            break
        else:
            # Send the user's message to the server
            client.send_message(message)

if __name__ == '__main__':
    main()
