from socket import *
import base64


serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(5)

print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    request = connectionSocket.recv(1024).decode()

    data = request[10:]
    message = base64.b64decode(data.encode())

    print(message.decode())
