import socket
import threading
from colorama import Fore, init

init(autoreset=True)

HOST = '127.0.0.1'
PORT = 12345

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

username = input("Enter your username: ")

def receive_messages():
    while True:
        try:
            msg = client.recv(1024).decode('utf-8')
            if msg == "USERNAME":
                client.send(username.encode('utf-8'))
            else:
                print(Fore.GREEN + msg)
        except:
            print(Fore.RED + "[ERROR] Disconnected from server.")
            client.close()
            break

def send_messages():
    while True:
        msg = input()
        message = f"{username}: {msg}"
        client.send(message.encode('utf-8'))

receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()

send_thread = threading.Thread(target=send_messages)
send_thread.start()
