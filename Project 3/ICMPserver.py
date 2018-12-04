from socket import *

serverPort = 13000
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

print("The server is ready to receive")

while True:
	print("hereAlso")
    connectionSocket, addr = serverSocket.accept()
    print("here")
    request = connectionSocket.recv(1024).decode()
    # where we put stuff to handle GET
    print(request)
    # print(request)

    #Sent stufff
    connectionSocket.send("this is a test".encode())
    connectionSocket.close()
