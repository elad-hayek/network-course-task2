from server import Client 
from _thread import *
import time

stop_recive = False

def recive_messages(client):
    while not stop_recive:
        client.receive_message()

def main():
    name = input("Enter your name: ")
    client = Client(name)
    client.connect_to_server('127.0.0.1', 65421)

    while True:
        global stop_recive
        stop_recive = False
       
        start_new_thread(recive_messages, (client,))

        message = input()
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
