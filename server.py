import socket
import threading

HOST = '127.0.0.1'
PORT = 12345

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
usernames = {}

def broadcast(message, _client=None):
    for client in clients:
        if client != _client:
            client.send(message)

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            broadcast(msg, client)
        except:
            index = clients.index(client)
            name = usernames[client]
            print(f"[OFFLINE] {name}")
            clients.remove(client)
            del usernames[client]
            client.close()
            broadcast(f"[{name} left the chat]".encode('utf-8'))
            break

def receive():
    print("[SERVER STARTED] Waiting for connections...")
    while True:
        client, addr = server.accept()
        print(f"[NEW CONNECTION] {addr}")

        client.send("USERNAME".encode('utf-8'))
        username = client.recv(1024).decode('utf-8')

        usernames[client] = username
        clients.append(client)

        print(f"[ONLINE] {username}")
        broadcast(f"{username} joined the chat!".encode('utf-8'))
        client.send("✅ Connected to the server!".encode('utf-8'))

        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

receive()
