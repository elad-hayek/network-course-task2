from server import Client 
from _thread import *
import time

MESSAGE = """Select an option:
    1. Create chat
    2. Join chat
    3. Close client
"""

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
        res = show_menu(client)
        if(res):
            break

        start_new_thread(recive_messages, (client,))

        while True:
            message = input()
            if(message == 'exit'):
                stop_recive = True
                client.send_message("EXIT_CHAT")
                break
            else:
                client.send_message(f"{message}&&chat_mode")


def show_menu(client):
    while True:
        message = input(MESSAGE)
        if (message == '1'):
            client.send_message_and_await_response("CREATE_CHAT")
            return False
        elif(message == '2'):
            chat_id = input("Enter chat id: ")
            client.send_message(f'JOIN_CHAT&&{chat_id}')
            data = client.receive_message()
            if(data == "Chat does not exist"):
                continue
            return False
        elif(message == '3'):
            client.send_message("CLOSE_CLIENT")
            global stop_recive
            stop_recive = True
            time.sleep(0.5)
            client.close()
            return True
        else:
            print("Invalid option")


if __name__ == '__main__':
    main()
