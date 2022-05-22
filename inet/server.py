import socket
from _thread import *

class Server:


    def __init__(self): 

        self.address = "192.168.1.124"

        self.port = 5555

    def start(self):

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

            start_new_thread(self.threaded_client, (conn,))

    def threaded_client(self, conn):

        conn.send(str.encode("Ansluten"))
        reply = ""

        while True:
            #try:
            data = conn.recv(2048)
            reply = data.decode("utf-8")

            if not data:
                print("Ifrånkopplad")
                break
            else:
                print("Mottog: ", reply)
                print("Skickar: ", reply)

            conn.sendall(str.encode(reply))
            #except:
            #    break

        print("Tappade anslutningen")
        conn.close()
            

def main():

    server = Server()
    server.start()


if __name__ == "__main__":
    main()
