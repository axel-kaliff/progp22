import socket
import curses
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
    screen = curses.initscr()

    data_received = c.client.recv(2048).decode()
    while True:
        try:
            screen.clear()
            screen.addstr(0,0,data_received)
            screen.refresh()
            data_received = c.client.recv(2048).decode()
        except socket.error as e:
            print(e)

def take_user_input(c):
    while True:

        event = keyboard.read_event()

        if keyboard.is_pressed("left"):
            c.send("LEFT")

        if keyboard.is_pressed("right"):
            c.send("RIGHT")

        if keyboard.is_pressed("up"):
            c.send("UP")

        if keyboard.is_pressed("down"):
            c.send("DOWN")



def main():

    client = Client("130.229.186.228")

    print(client.connect())

    threads = []

    t1 = threading.Thread(target=update_game, args=(client, ))
    t1.daemon = True
    t1.start()

    take_user_input(client)
        
if __name__ == "__main__":
    main()


