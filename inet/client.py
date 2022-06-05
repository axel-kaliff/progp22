import socket
import keyboard
import sys
from _thread import *
import threading

class Client:


    def __init__(self, server="192.168.1.163"):

        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.port = 5555

        self.server = server
        self.addr = (self.server, self.port)


    def connect(self):

        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()
        except:
            pass

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return "sent command"
            #return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

def update_game(c):
    while True:
        try:
            data_received = c.client.recv(2048).decode()
            print(data_received)
        except socket.error as e:
            print(e)

def take_user_input(c):
    while True:
        user_input = input()
        if user_input.strip() == "d":
            print(c.send("RIGHT"))
        elif user_input.strip() == "a":
            print(c.send("LEFT"))
        elif user_input.strip() == "s":
            print(c.send("DOWN"))
        elif user_input.strip() == "w":
            print(c.send("UP"))



def main():

    client = Client("192.168.1.163")

    print(client.connect())

    threads = []

    t1 = threading.Thread(target=update_game, args=(client, ))
    t1.daemon = True
    t1.start()

    take_user_input(client)
    #t2.start()

    #t2 = threading.Thread(target=take_user_input, args=(client, ))
    #t2.join()

    #start_new_thread(update_game, (client, ))
    #start_new_thread(take_user_input, (client, ))
        
if __name__ == "__main__":
    main()


