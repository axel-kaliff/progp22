import socket
import keyboard
import sys
from _thread import *

class Client:


    def __init__(self, server="192.168.0.191"):

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
        print("sending")

        try:
            self.client.send(str.encode(data))
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)

    def update_game(self, 


def main():

    client = Client("192.168.0.191")

    print(client.connect())


    while True:
        # ska det här skapas trådar för input/output?

        # TODO split into two threads so it can wait for user input and update when the other user moves

        start_new_thread(update_game, (conn, current_player))
        user_input = input()

        if user_input.strip() == "d":
            print(client.send("RIGHT"))
        elif user_input.strip() == "a":
            print(client.send("LEFT"))
        elif user_input.strip() == "s":
            print(client.send("DOWN"))
        elif user_input.strip() == "w":
            print(client.send("UP"))


if __name__ == "__main__":
    main()


