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
        except socket.error as e:
            print(e)

def update_game(c):
    screen = curses.initscr()

    data_received = c.client.recv(2048).decode()
    
    while True:
        try:
            screen.clear()

            info = data_received.split("|")

            screen.refresh()

            for wall in info[0].split(" "):
                wall_pos = wall.split(",")
                wall_x = int(wall_pos[0])
                wall_y = int(wall_pos[1])
                screen.addstr(wall_x, wall_y, "W")

            key_pos = info[1].split(",")
            key_x = int(key_pos[0])
            key_y = int(key_pos[1])

            if info[2] == "0,0":
                screen.addstr(key_x, key_y, "K")

            plate_door_info = info[3].split(",")
            if plate_door_info[0] == "1":
                screen.addstr(int(plate_door_info[1]), int(plate_door_info[2]), "D")

            key_door_info = info[4].split(",")
            if key_door_info[0] == "1":
                screen.addstr(int(key_door_info[1]), int(key_door_info[2]), "D")

            for (number, player) in enumerate(info[6].split(" ")):
                player_pos = wall.split(",")
                player_x = int(wall_pos[0])
                player_y = int(wall_pos[1])
                if number == 0:
                    screen.addstr(wall_x, wall_y, "1")
                else:
                    screen.addstr(wall_x, wall_y, "2")

            if info[5] == "1":
                screen.clear()
                screen.addstr("GAME OVER")

            if info[7] == "1":
                screen.clear()
                screen.addstr("WAITING FOR 1 MORE PLAYER")
            

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
    print("hi")

    client = Client("192.168.1.163")

    print(client.connect())

    threads = []

    t1 = threading.Thread(target=update_game, args=(client, ))
    t1.daemon = True
    t1.start()

    take_user_input(client)
        
if __name__ == "__main__":
    main()


