#! /usr/bin/python
# Client program
import socket, sys, re, os
from EncapFramedSock import EncapFramedSock

sys.path.append("../lib")       # for params
import params



switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

print("Lab 2 File-Transfer")

while True:
    try:
        fileName = input("Enter file name to send: ")
        file = open("./FilesToSend/" + fileName, "rb")
        break
    except FileNotFoundError:
        print(fileName + " does not exist, Try again")

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

addrPort = (serverHost, serverPort)

listen_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if listen_socket is None:
    print('could not open socket')
    sys.exit(1)

listen_socket.connect(addrPort)

encapSock = EncapFramedSock((listen_socket, addrPort))

fileContents = file.read()

if len(fileContents) == 0:
    print("File is empty, exiting")
    sys.exit(1)

print("sending " + fileName)

encapSock.send(fileName, fileContents, debug)
