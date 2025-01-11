from server import Client 

MESSAGE = """Select an option:
    1. Create chat
    2. Join chat
    3. Exit chat
    4. Close client
"""

def main():
    name = input("Enter your name: ")
    client = Client(name)
    client.connect_to_server('127.0.0.1', 65421)

    while True:
        res = show_menu(client)
        if(res):
            break

        while True:
            message = input("Enter message: ")
            if(message == 'exit'):
                client.send_message_and_await_response("EXIT_CHAT")
                break
            else:
                client.send_message(message)



def show_menu(client):
    while True:
        message = input(MESSAGE)
        if (message == '1'):
            client.send_message_and_await_response("CREATE_CHAT")
            return False
        elif(message == '2'):
            chat_id = input("Enter chat id: ")
            client.send_message_and_await_response(f'JOIN_CHAT&&{chat_id}')
            return False
        elif(message == '3'):
            client.send_message_and_await_response("EXIT_CHAT")
            return False
        elif(message == '4'):
            client.send_message("BYE")
            client.close()
            return True
        else:
            print("Invalid option")


if __name__ == '__main__':
    main()
