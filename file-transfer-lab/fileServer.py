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
while True:
    print("listening on:", bindAddr)

    sock, addr = lsock.accept()
    
    if not os.fork():

        print("connection rec'd from", addr)

        payload = framedReceive(sock, debug)
        if debug:
            print("rec'd: ", payload)

        if not payload:
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
            
            
            