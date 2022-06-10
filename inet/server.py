import socket
from _thread import *
from game import Game


class Server:

    current_player = 0
    game = Game()


    def __init__(self): 

        self.address = "130.229.185.52"
        self.port = 5555
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

    def threaded_client(self, conn, player):

        conn.send(str.encode("Ansluten"))
        reply = ""
        self.game.add_player()

        while True:
            data = conn.recv(2048)
            print("data recieved")
            print("data: {d}".format(d=data))
            command = data.decode("utf-8")
            
            if self.game.player1 and self.game.player2:
                self.game.move(player + 1, command)

            if not data:
                print("Ifrånkopplad")
                break
            else:
                if self.game.game_won:
                    reply = "1"
                elif (not self.game.player1) or (not self.game.player2):
                    reply = "0"
                else:
                    reply = self.game.print_state()
             
                print("Mottog: ", command)
                #print("Skickar: ", reply)

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
