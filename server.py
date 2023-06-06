import socket
from _thread import *
from tile import Tile
import sys
import pickle

server = '127.0.0.1'
port = 5555
players = {}

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
    while True:
        try:
            #print("waiting for data")
            data = conn.recv(2048)
            if data:
                print("recieved data from player ", player)
                send_all(data, player)
                response_object = pickle.loads(data)
                print(response_object)
        except:
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