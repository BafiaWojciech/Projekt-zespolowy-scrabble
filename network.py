import socket
import traceback

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #self.client.settimeout(1.0)
        self.server = "127.0.0.1"
        self.port = 5555
        self.addr = (self.server, self.port)
        
        self.pos = self.connect()
    

    def getPos(self):
        return self.pos

    def recv(self):
        try:
            return self.client.recv(2048)
        except socket.error as e:
            print("recv err: ",e)
            print(traceback.format_exc())

    def connect(self):
        try:
            self.client.connect(self.addr)
        except:
            pass

    def send(self, data):
        try:
            self.client.send(data)
        except socket.error as e:
            print("send err: ",e)
            print(traceback.format_exc())