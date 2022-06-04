import socket
from _thread import *


class Server:

    pos = [(0,0), (100,100)]

    def __init__(self): 

        self.address = "192.168.0.191"
        self.port = 5555
        self.pos = [[0,0], [100,100]]

    def start(self):

        current_player = 0

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            s.bind((self.address, self.port))
        except socket.error as e:
            print(str(e))

        # marks socket as passive socket, accepts incoming connection requests
        s.listen(2)
        
        print("Servern är igång")


        while True:

            conn, addr = s.accept()

            print(f"{addr} ansluten")

            #TODO start threads so it can be connected to two

            start_new_thread(self.threaded_client, (conn, current_player))

            current_player += 1


    def make_move(self, command, player):
        if command == "UP" and not self.pos[player][1] == 0:
           self.pos[player][1] -= 1
        elif command == "DOWN" and not self.pos[player][1] == 100:
            self.pos[player][1] += 1
        elif command == "LEFT" and not self.pos[player][0] == 0:
            self.pos[player][0] -= 1
        elif command == "RIGHT" and not self.pos[player][0] == 100:
            self.pos[player][0] += 1
            

    def threaded_client(self, conn, player):

        conn.send(str.encode("Ansluten"))
        reply = ""

        while True:
            #try:
            data = conn.recv(2048)
            print("data recieved")
            print("data: {d}".format(d=data))
            command = data.decode("utf-8")
            
            self.make_move(command, player)

            if not data:
                print("Ifrånkopplad")
                break
            else:
                reply = "Player 0: ( {player_one_x} , {player_one_y} ). Player 1: ({player_two_x} , {player_two_y})".format(player_one_x = self.pos[0][0], player_one_y = self.pos[0][1], player_two_x = self.pos[1][0], player_two_y = self.pos[1][1])

                print("Mottog: ", command)
                print("Skickar: ", reply)

            
            conn.sendall(str.encode(reply))

        print("Tappade anslutningen")
        conn.close()
            

def main():

    server = Server()
    server.start()


if __name__ == "__main__":
    main()
