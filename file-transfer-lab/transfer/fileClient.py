#! /usr/bin/env python3

import socket, sys, re

sys.path.append("../../lib")       # for params
import params

sys.path.append("../../framed-echo")
from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )
    
progName = "fileClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug  = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()
    
try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)

if s is None:
    print('could not open socket')
    sys.exit(1)

s.connect(addrPort)
try:
    userInput = input("Please put a text file you would like to send.\n")
    fc = open(userInput, "rb")
except FileNotFoundError:
    print("  not found")
    sys.exit(1)

words = fc.read()

if len(words) == 0:
    print("Contents of file were empty")
    sys.exit(1)

print("sending " + userInput)
framedSend(s, (userInput + "<" + str(words)).encode(), debug)
    
    
    
    
    
    
    
