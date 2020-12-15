#! /usr/bin/env python3

import sys
from EncapFramedSock import EncapFramedSock

sys.path.append("../lib")  # for params
import re, socket, params, os

from threading import Thread, Lock

current_files = set()

lock = Lock()


def file_transfer_start(fname):
    global current_files, lock
    lock.acquire()
    if fname in current_files:
        print("File is currently being written to")
        lock.release()
        sys.exit(1)
    else:
        current_files.add(fname)
        lock.release()


def file_transfer_end(fname):
    global current_files, lock
    lock.acquire()
    current_files.remove(fname)
    lock.release()


switchesVarDefaults = (
    (('-l', '--listenPort'), 'listenPort', 50001),
    (('-d', '--debug'), "debug", False),  # boolean (set if present)
    (('-?', '--usage'), "usage", False),  # boolean (set if present)
)

paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']

if paramMap['usage']:
    params.usage()

lsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # listener socket
bindAddr = ("127.0.0.1", listenPort)
lsock.bind(bindAddr)
lsock.listen(5)
print("listening on:", bindAddr)


class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.sock, self.addr = sockAddr
        self.fsock = EncapFramedSock(sockAddr)

    def run(self):
        print("new thread handling connection from", self.addr)
        while True:
            try:
                fileName, fileContents = self.fsock.receive(debug)
            except:
                print("File transfer failed")
                sys.exit(1)

            if debug: print("rec'd: ", fileContents)

            if fileContents is None:
                print("Empty file! Exiting.")
                sys.exit(1)

            fileName = fileName.decode()


            try:
                if not os.path.exists("./ReceivedFiles/" + fileName):
                    
                    file_transfer_start(fileName)
                    file = open("./ReceivedFiles/" + fileName, 'w+b')
                    # print("FC:", fileContents)
                    file.write(fileContents)
                    file.close()
                    # print(8)
                    print("File", fileName, "successfully accepted!")
                    file_transfer_end(fileName)
                    sys.exit(0)
                else:
                    print("File with name", fileName, "already exists on server. exiting...")
                    sys.exit(1)
            except FileNotFoundError:
                print("Fail")
                sys.exit(1)


while True:
    sockAddr = lsock.accept()
    server = Server(sockAddr)
    server.start()
