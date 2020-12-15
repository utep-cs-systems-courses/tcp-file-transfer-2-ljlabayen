#! /usr/bin/env python3

import sys
sys.path.append("../lib")       # for params
import re, socket, params, os

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
print("listening on:", bindAddr)


while True:
    sock, addr = lsock.accept()
    
    from framedSock import framedSend, framedReceive

    if not os.fork():
        print("connected from", addr)

        payload = ""
        try:
            fileName, fileContents = framedReceive(sock, debug)
        except:
            print("File transfer failed")
            sys.exit(1)

        if debug: print("rec'd: ", payload)

        if payload is None:
            print("File is empty! Exiting")
            sys.exit(1)

        fileName = fileName.decode()

        try:
            if not os.path.isfile("./IncomingFiles/" + fileName):
                file = open("./IncomingFiles/" + fileName, "wb+")
                file.write(fileContents)
                file.close()
                print("File", fileName, "accepted!")
                sys.exit(0)
            else:
                print(fileName, "is in IncomingFiles folder. Exiting")
                sys.exit(1)
        except FileNotFoundError:
            print("Fail. Exiting")
            sys.exit(1)
