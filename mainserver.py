import threading
import socket

#host = '127.0.0.1' # localhost
host = '149.84.185.191' # actual IP address
port = 55555 # random, likely unused socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #Internet socket, TCP
server.bind((host, port))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def handle(client): # Function to handle client messages
    while True:
        try:
            message = client.recv(1024) 
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast (f'{nickname} left the chat!'.encode('ascii'))
            nicknames.remove(nickname)
            break

def receive(): # Function to receive client messages
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}")

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of the client is {nickname}!')
        broadcast(f'{nickname} joined the chat!'.encode('ascii'))
        client.send('Connected to the server!'.encode('ascii'))

        thread = threading.Thread(target=handle, args =(client,))
        thread.start()

print("Server is online")
receive()
