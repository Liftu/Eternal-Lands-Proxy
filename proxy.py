#!/usr/bin/python2
# -*- coding: Utf-8 -*-
# Fichier : proxy.py

import socket, os, parser
from threading import Thread
#from importlib import reload

###############################################################
# Cette classe est un thread servant de client au vrai serveur
# et renvoi le traffic du vrai serveur vers le vrai client (Client2Proxy).
class Proxy2Server(Thread):

        def __init__(self, host, port):
            super(Proxy2Server, self).__init__() #for python 2
            #super().__init__() # Appel la le constructeur de l'objet herite (Thread)
            self.client = None # Socket vers le client
            self.port = port
            self.host = host
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.connect((host, port))

        # Lance le thread
        def run(self):
            while True:
                data = self.server.recv(4096)
                if data:
                    try:
                        parser.parse(data, 'server')
                        #print("### %i ###" %(len(parser.CLIENT_QUEUE)))
                        if len(parser.CLIENT_QUEUE) > 0:
                            pkt = parser.CLIENT_QUEUE.pop()
                            print("got queue client: {}".format(pkt.encode('hex')))
                            # self.game.sendall(pkt)
                    except Exception as e:
                        print("server[%s]" %(e))
                    #Envoyer vers le client
                    self.client.sendall(data)


###############################################################
# Cette classe est un thread servant de serveur au vrai client
# et renvoi le traffic du vrai client vers le vrai serveur (Proxy2Server).
class Client2Proxy(Thread):

        def __init__(self, host, port):
            super(Client2Proxy, self).__init__()
            self.server = None  # real server socket not known yet
            self.port = port
            self.host = host
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind((host, port))
            sock.listen(1)
            # waiting for a connection
            self.client, addr = sock.accept()

        # Lance le thread
        def run(self):
            while True:
                data = self.client.recv(4096)
                if data:
                    try:
                        parser.parse(data, 'client')
                        if len(parser.SERVER_QUEUE) > 0:
                            pkt = parser.SERVER_QUEUE.pop()
                            print("got queue server: {}".format(pkt.encode('hex')))
                            # self.server.sendall(pkt)
                    except Exception as e:
                        print("client[%s]" %(e))
                    #Envoyer vers le serveur
                    self.server.sendall(data)


###############################################################
class Proxy(Thread):

    def __init__(self, from_host, to_host, port):
        super(Proxy, self).__init__() # for python 2
        #super().__init__()  # Appel la le constructeur de l'objet herite (Thread)
        self.from_host = from_host
        self.to_host = to_host
        self.from_port = port
        self.to_port = port
        self.running = False

    # Lance le thread
    def run(self):
        while True:
            print("[proxy(%i)] Setting up..." %(self.from_port))
            self.c2p = Client2Proxy(self.from_host, self.from_port)
            self.p2s = Proxy2Server(self.to_host, self.to_port)

            self.c2p.server = self.p2s.server # Connecte le vrai client
            self.p2s.client = self.c2p.client # et le vrai serveur ensemble.
            self.running = True
            print("Starting threads...")

            self.c2p.start()
            self.p2s.start()
            print("[proxy(%i)] Connection established." %(self.from_port))


if __name__ == "__main__":
    proxy = Proxy("0.0.0.0", "62.93.225.45", 3000)
    proxy.start()

    while True:
        try:
            cmd = raw_input('')
            if cmd[:4] == 'quit':
                os._exit(0)
            elif cmd[:2] == "C ":
                # Send cmd to server
                if proxy.running:
                    print(cmd[2:].decode('hex'))
                    parser.CLIENT_QUEUE.append(cmd[2:].decode('hex'))
            elif cmd[:2] == "S ":
                # Send cmd to client
                if proxy.running:
                    proxy.c2p.client.sendall(cmd[2:].decode('hex'))
            else:
                reload(parser)
        except Exception as e:
            print(e)
