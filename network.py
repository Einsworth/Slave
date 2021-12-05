#   network module contain the network class that use for connecting to the server
#
#   Created by Thanawat Patite ID 62070501027 (Nov 11, 2021)

#---------- import setting ----------#
import socket
import pickle

#---------- class setting ----------#

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "26.12.84.96" #server IPV4
        self.port = 5555    #server port
        self.addr = (self.server, self.port)    #server address
        self.id = self.connect()    #connection id

    #this function return id of this Network
    #return id of this Network
    def getPlayer(self):
        return self.id

    #this function make client connects to the server
    #return data receive from the server
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass
    
    #this function send data to the server
    #   data is the data that client want to send to the server
    #return data receive from the server
    def send(self, data):
        try:
            self.client.send(pickle.dumps(data))
            #print("Send data to server: " ,data)
            return pickle.loads(self.client.recv(2048*2))
        except socket.error as e:
            print(e)

    #this function make client disconnect from the server
    def disconnect(self):
        try:
            self.client.shutdown(2)
            self.client.close()
        except:
            pass