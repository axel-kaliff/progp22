import socket
import curses
import keyboard
import sys
from _thread import *
import threading

class Client:

    # OLIVIA
    #def __init__(self, server="130.229.171.227"): 
    #GRACE
    def __init__(self, server="130.229.185.52"):
        # setting up for a connection to server
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.port = 5555
        self.server = server
        self.addr = (self.server, self.port)

    def connect(self):
        # attempt connection and return server response
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

# This function splits data according to protocoll given and prints results to curses screen
def print_map(screen, data):
        info = data.split("|")

        screen.refresh()

        # print "w" at every wall location
        for wall in info[0].split(" ")[:-1]:
            wall_pos = wall.split(",")
            wall_x = int(wall_pos[0])
            wall_y = int(wall_pos[1])
            screen.addstr(wall_x, wall_y, "w")

        # print "D" at every door location
        for door in info[1].split(" ")[:-1]:
            door_pos = door.split(",")
            screen.addstr(int(door_pos[0]), int(door_pos[1]), "D")


        # print key to map
        if not info[2] == " ":
            key_pos = info[2].split(",")
            key_x = int(key_pos[0])
            key_y = int(key_pos[1])
            screen.addstr(key_x, key_y, "K")

        # print "T" for "Trophy" at trophy location
        prize_pos = info[3].split(",")
        screen.addstr(int(prize_pos[0]), int(prize_pos[1]), "T")

        # print "P" for pressure plate
        pressure_pos = info[4].split(",")
        screen.addstr(int(pressure_pos[0]), int(pressure_pos[1]), "P")

        
        # print player locations
        for (number, player) in enumerate(info[5].split(" ")[:-1]):
            player_pos = player.split(",")
            player_x = int(player_pos[0])
            player_y = int(player_pos[1])
            if number == 0:
                screen.addstr(player_x, player_y, "1")
            else:
                screen.addstr(player_x, player_y, "2")

def update_game(c):
    # start curses screen
    screen = curses.initscr()

    data_received = c.client.recv(2048).decode()
    
    # Repeats throughout game
    while True:
        try:
            #reset screen
            screen.clear()
            if data_received == "0":
                screen.addstr(0, 0, "WAITING FOR 1 MORE PLAYER")
            elif data_received == "1":
                screen.addstr(0, 0, "GAME WON!!!!")
            else:
                print_map(screen, data_received)
            
            #update screen
            screen.refresh()

            # stops here until data is received
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
    # GRACE
    client = Client("130.229.185.52")
    #OLIVIA
    client = Client("130.229.171.227")

    print(client.connect())

    # start new thread for updating game
    t1 = threading.Thread(target=update_game, args=(client, ))
    # run thread in background, does not need to sync with any other thread
    t1.daemon = True
    t1.start()

    take_user_input(client)
        
if __name__ == "__main__":
    main()


