#! /usr/bin/env python3

# Echo client program
import socket, sys, re, os

sys.path.append("../lib")       # for params
import params
from framedSock import framedSend, framedReceive


switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )
tryCount = 0
while True and (tryCount < 10):
    try:
        fileName = input("Enter file name to be sent to server: ")
        file = open("./OutFiles/" + fileName, "rb")
        break
    except FileNotFoundError:
        print("File does not exist, please enter another file name to try again")
        tryCount += 1
if tryCount >= 10:
    sys.exit(1)
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

fileContents = file.read()

if len(fileContents) == 0:
    print("File is empty, exiting")
    sys.exit(1)

print("sending", fileName)

framedSend(s, fileName, fileContents, debug)
