import socket
import pickle

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "26.12.84.96"         #server IPV4
        self.port = 5555                    #server port
        self.addr = (self.server, self.port)
        self.id = self.connect()

    def getPlayer(self):
        return self.id

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            #print("Send data to server: " ,data)
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)