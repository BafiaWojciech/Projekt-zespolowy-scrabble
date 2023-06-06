import socket
from _thread import *
from tile import Tile
import sys
import pickle

SIGNAL_WRONG_TURN = -1
SIGNAL_OK = 0
SIGNAL_PASS = -2
SIGNAL_END_GAME = -3

server = '127.0.0.1'
port = 5555
players = {}
curr_player = 0

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
try:
    s.bind((server, port))
except socket.error as e:
    print(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def send_all(obj, exc_player): #send to all (except the original sender)
    print("exc_player ", exc_player)
    for player, sock in players.items():
        if player != exc_player:
            print("sending to player ", player)
            sock.sendall(obj)

pos = [(0,0),(100,100)]

def threaded_client(conn, player):
    global curr_player
    while True:
        try:
            data = conn.recv(2048)
            if data:
                if player != curr_player:
                    players[player].sendall(pickle.dumps(SIGNAL_WRONG_TURN))
                else:
                    players[player].sendall(pickle.dumps(SIGNAL_OK))
                    print("recieved data from player ", player)
                    send_all(data, player)
                    response_object = pickle.loads(data)
                    print(response_object)
                    curr_player += 1
                    if curr_player >= len(players):
                        curr_player = 0
        except Exception as exc:
            print(exc)
            break
    print("Lost connection")
    conn.close()

while True:
    print("waiting for conns")
    sock, _ = s.accept()
    player_no = len(players)
    players[player_no] = sock
    print("Connected to:", player_no)
    start_new_thread(threaded_client, (sock, player_no))