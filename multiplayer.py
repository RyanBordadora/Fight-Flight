import threading
import socket
import time 
import select
import sys

HOST = socket.gethostbyname(socket.gethostname())
print(HOST)
PORT = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
user_ids = []
nicknames = []
uid_bank = []
rdy_bank = []
global team1_score, team2_score
team1_score = 10
team2_score = 10
lock = threading.Lock()
def broadcast(message):
    with lock:
        for client in clients:
            client.sendall(message)
    sys.stdout.flush()

def handle(client):
    global team1_score, team2_score
    while True:
        try:
            message = client.recv(1024)
            if message:
                if message.startswith(b"CHANGETEAM"):  # Check if message is to change team
                    new_team_id = int(message.decode().split()[1])  # Extract new team ID from message
                    index = clients.index(client)
                    nicknames[index] = nicknames[index][:-1] + str(new_team_id)
                    broadcast_player_update()  # Broadcast updated player information
                    time.sleep(0.1)
                    rdy_bank[index] = 0
                    time.sleep(0.1)
                    
                    broadcast_ready_update()

                elif message.startswith(b"READY"):
                    index = clients.index(client)
                    rdy_bank[index] = 1
                    broadcast_ready_update()
                    sys.stdout.flush()
                elif message.startswith(b"UID_Request"):
                    index = clients.index(client)
                    client.send(f'UID:{user_ids[index]}'.encode('ascii'))
                elif message == "RU":
                    broadcast_player_update()
                    print(f"CR{message}")
                elif message.startswith(b"SCOREUPDATE"):
                    print("Received", message)
                    score = int(message.decode().split()[1])  # Extract new team ID from message
                    index = clients.index(client)
                    print("Scoresplit: ", score)
                    if int(nicknames[index][-1]) == 1:
                        team1_score = team1_score + score
                    else:
                        team2_score = team2_score + score
                    broadcast(f'Score:{team1_score}/{team2_score}'.encode('ascii'))
                else:
                    broadcast(message)
                    print(message)
                sys.stdout.flush()
        except Exception as e:
            print(f"Error: {e}")
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.pop(index)
            user_id = user_ids[index]
            user_ids.pop(index)
            rdy_bank.pop(index)
            uid_bank.append(user_id)
            broadcast_player_update()
            uid_bank.sort()
            broadcast(f'{nickname} has left the game!\n'.encode('ascii'))
            break

def broadcast_player_update():
    player_list = [f'{nickname}{user_id}' for nickname, user_id in zip(nicknames, user_ids)]
    player_update_msg = f"Player Update:{','.join(player_list)} \n"
    print(player_update_msg)
    broadcast(player_update_msg.encode('ascii'))
    sys.stdout.flush()

def broadcast_ready_update():
    ready_list = [f'{ready}{user_id}' for ready, user_id in zip(rdy_bank, user_ids)]
    player_update_msg = f"Ready Update:{','.join(ready_list)} \n"
    print(player_update_msg)
    broadcast(player_update_msg.encode('ascii'))
    sys.stdout.flush()


def receive():
    while True:
        # Use select to check if there's incoming data
        readable, _, _ = select.select([server], [], [], 0.1)
        for client in readable:
            client, address = server.accept()
            print(f"Connected with {str(address)} \n")

            client.send('NICK'.encode('ascii'))
            nickname = client.recv(1024).decode('ascii')
            nicknames.append(nickname)

            # Assign user ID
            if uid_bank:
                user_id = uid_bank.pop(0)  # Reuse the first available user ID
            else:
                user_id = len(clients)  # Use index as user ID if no IDs available
            user_ids.append(user_id)

            clients.append(client)
            rdy_bank.append(0)
            nickname_with_id = f"{nickname}{user_id}"  # Append user ID to nickname
            print(f'Nickname of the client is {nickname_with_id}! \n')
            broadcast_player_update()
            time.sleep(0.1)
            broadcast_ready_update()
            time.sleep(0.1)
            broadcast(f'{nickname_with_id} joined the game! \n'.encode('ascii'))
            time.sleep(0.1)
            client.sendall('Connected to the server! \n'.encode('ascii'))
            sys.stdout.flush()
            thread = threading.Thread(target=handle, args=(client,))
            thread.start()
            print("Connected!")
            sys.stdout.flush()

        # Continue other operations here
        # For example, handling keyboard interrupts

    # Close the server and clients when loop breaks


try:
    print("Server is listening!...")
    receive()
except KeyboardInterrupt:
    print("Server shutting down...")
    server.close()
    for client in clients:
        client.close()
