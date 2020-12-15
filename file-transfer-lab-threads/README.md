# File Transfer With Threads

This is the implementation of the file transfer server using Threads. 

# To Run 
First run the file transfer server with ./fileServer.py and then run the client with ./fileClient.py. 
All files to be transfered are within the folder "FilesToSend"
To run with the Stammer proxy, first run the proxy from it's directory with ./stammerProxy.py, then run ./fileServer.py. Lastly run ./fileClient.py -s 127.0.0.1:50000

This version handles:
* Zero length files
* Works with and without the proxy
* File already exists on the server
* Client or server unexpectedly disconnect
* Two clients try to transfer the same file at the same time
