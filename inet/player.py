import keyboard
from client import Client

class Player:

    def __init__(self):

        self.client = Client()
        self.client.connect()

    def start_game(self):

        while True:

            event = keyboard.read_event()

            if keyboard.is_pressed("left"):
                self.client.send("left")

            if keyboard.is_pressed("right"):
                self.client.send("right")

            if keyboard.is_pressed("up"):
                self.client.send("up")

            if keyboard.is_pressed("down"):
                self.client.send("down")


def main():
    player = Player()
    player.start_game()

if __name__ == "__main__":
    main()
        
