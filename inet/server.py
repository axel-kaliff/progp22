import socket
from _thread import *


class Server:

    pos = [(0,0), (25,25)]
    current_player = 0

    def __init__(self): 

        self.address = "192.168.1.163"
        self.port = 5555
        self.pos = [[0,0], [100,100]]
        self.connections = []
        self.current_player = 0

    def start(self):

        self.current_player = 0

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

            start_new_thread(self.threaded_client, (conn, self.current_player))

            self.connections.append(conn)

            self.current_player += 1


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

                # wall positions
                reply = "0,3 0,1 1,1 1,2 1,3 1,4"
                # key position
                reply += "|" + "4,4"
                # player/key status
                reply += "|" + "0,0"
                # plate door status and position
                reply += "|" + "1,5,5"
                # key door status and position
                reply += "|" + "1,2,2"
                # win status
                reply += "|" + "1"
                # player positions
                reply += "|" + "0,0 10,10"

                # number of current players
                reply += "|" + str(self.current_player)


                print("Mottog: ", command)
                print("Skickar: ", reply)

            
            for connection in self.connections:
                connection.sendall(str.encode(reply))

        print("Tappade anslutningen")
        self.current_player -= 1
        self.connections.remove(conn)
        conn.close()
            

def main():

    server = Server()
    server.start()


if __name__ == "__main__":
    main()
