#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os
sys.path.append("../framed-echo")
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)

from threading import Thread, Lock

lock = Lock()

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            print("listening on:", bindAddr)
    
            print("connection rec'd from", self.addr)

            lock.acquire()
            payload = framedReceive(self.sock, debug)
            if debug:
                print("rec'd: ", payload)

            if not payload:
                lock.release()
                sys.exit(1)
            
            payload = payload.decode()

            name = payload.split("<")[0]
            content = payload.split("<")[1].encode()
            
            try:
                if not os.path.isfile(name):
                    file = open(name, 'wb+')
                    file.write(content)
                    file.close()
                else:
                    print("File with name", name, "already exists on server. exiting...")
            except FileNotFoundError:
                print("Fail")
            lock.release()


while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()