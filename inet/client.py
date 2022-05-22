import socket
import sys

class Client:

    def __init__(self, server="192.168.1.124"):

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
            return self.client.recv(2048).decode()
        except socket.error as e:
            print(e)


def main():

    client = Client("192.168.1.124")

    print(client.connect())

    while True:
        if input() == "o":
            client.send("hi")
            client.send("ho")


if __name__ == "__main__":
    main()


