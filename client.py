from client_class import Client 
from _thread import *
import time

stop_recive = False

def recive_messages(client):
    global stop_recive
    while not stop_recive:
        try:
            client.receive_message()
        except Exception:
            stop_recive = True

def main():
    name = input("Enter your name: ")
    client = Client(name)
    client.connect_to_server('127.0.0.1', 65421)

    global stop_recive
    while not stop_recive:
       
        start_new_thread(recive_messages, (client,))

        message = input()

        if(stop_recive):
            print(f"Sorry, {client.name} The server is not available!")
            client.close()
            break

        if(message == 'exit'):
            stop_recive = True
            client.send_message("CLOSE_CLIENT")
            time.sleep(0.5)
            client.close()
            break
        else:
            client.send_message(message)



if __name__ == '__main__':
    main()
