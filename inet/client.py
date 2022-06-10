import socket
import curses
import keyboard
import sys
from _thread import *
import threading

class Client:


    def __init__(self, server="130.229.185.52"):

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

def print_map(screen, data):
        info = data.split("|")

        screen.refresh()

        for wall in info[0].split(" ")[:-1]:
            wall_pos = wall.split(",")
            wall_x = int(wall_pos[0])
            wall_y = int(wall_pos[1])
            screen.addstr(wall_x, wall_y, "w")

        for door in info[1].split(" ")[:-1]:
            door_pos = door.split(",")
            screen.addstr(int(door_pos[0]), int(door_pos[1]), "D")


        if not info[2] == " ":
            key_pos = info[2].split(",")
            key_x = int(key_pos[0])
            key_y = int(key_pos[1])
            screen.addstr(key_x, key_y, "K")

        prize_pos = info[3].split(",")
        screen.addstr(int(prize_pos[0]), int(prize_pos[1]), "T")

        pressure_pos = info[4].split(",")
        screen.addstr(int(pressure_pos[0]), int(pressure_pos[1]), "P")

        
        for (number, player) in enumerate(info[5].split(" ")[:-1]):
            player_pos = player.split(",")
            player_x = int(player_pos[0])
            player_y = int(player_pos[1])
            if number == 0:
                screen.addstr(player_x, player_y, "1")
            else:
                screen.addstr(player_x, player_y, "2")

def update_game(c):
    screen = curses.initscr()

    data_received = c.client.recv(2048).decode()
    
    while True:
        try:
            screen.clear()
            if data_received == "0":
                screen.addstr(0, 0, "WAITING FOR 1 MORE PLAYER")
            elif data_received == "1":
                screen.addstr(0, 0, "GAME WON!!!!")
            else:
                print_map(screen, data_received)
            
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

    client = Client("130.229.185.52")

    print(client.connect())

    threads = []

    t1 = threading.Thread(target=update_game, args=(client, ))
    t1.daemon = True
    t1.start()

    take_user_input(client)
        
if __name__ == "__main__":
    main()


