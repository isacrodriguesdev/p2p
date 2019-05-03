import socket
import random
import selectors
from time import sleep
import datetime as Date
import threading
import os
import sys
import json

host = socket.socket.gethostbyname(socket.gethostname)
port = 4000
peers = [
   {'host': '172.19.253.193', 'port': 4000},
   {'host': '172.19.253.193', 'port': 4000}
   ]
peers_received = []

class Cliente():

    def __init__(self):

      # t = threading.Thread(
      #    target=self.start, 
      #    name="search")

      self.start()

      while 1:
         sleep(20)
         self.start()

    def seendPeers(self, conn):
      so = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      for i in range(len(peers)):
         peers_ip = []

         peers_ip.append({
            "host": peers[i][0],
            "port": peers[i][1],
            "date": str(Date.datetime.now())
         })

      for ii in range(len(peers)):
         socket.socket.sendto(conn, json.dumps(peers_ip).encode(), peers[ii])

    def start(self):

        loop = 0

        while loop < len(peers):
            sleep(2)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            try:
                seend = s.connect_ex((peers[loop]['host'], peers[loop]['port']))
                if seend == 0:
                    print('Connected in', peers[loop][1])
                    loop += 1
                    self.seendPeers(s)
                    s.close()
            except Exception as e:
                print(e)


class Server():

    def __init__(self):

        threading.Thread(target=self.start, name="listener").start()

    def start(self):

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        s.bind((host, port))
        s.listen(5)

        while True:
            conn, addr = s.accept()
            try:
               data = conn.recv(1024)
               peers_received = json.loads(data)
               print('>> ', peers_received)
               s.close()
               conn.setblocking(False)
               if data:
                  peers_received = json.loads(data)
                  print('>> ', peers_received)
            except Exception as e:
               pass

            if addr:
                if len(peers) > 0:
                    for i in range(len(peers)):
                        if peers[i]['host'] == peers_received[i]['port']:
                            continue
                        else:
                           peers.append(peers_received)
                else:
                    peers.append(peers_received)

            print(peers_received)
            # self.setPeers()

    def setPeers(self):
        with open('peers.dat', 'r') as f:

            p = f.readlines()
            dat = open('peers.dat', 'a')

            if len(p) > 0:
                for i in range(len(p)):
                    for ii in range(len(peers)):
                        if p[i] == peers[ii][0]:
                            continue
                        else:
                            dat.write(peers[i][0])
                            dat.write('\n')
                dat.close()
            else:
                for i in range(len(peers)):
                    dat.write(peers[i][0])
                    dat.write('\n')
                dat.close()


listener = Server()
search = Cliente()

# print(threading.enumerate())
