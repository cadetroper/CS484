from socket import *

serverName = 'localhost'
serverPort = 13000

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
message = input('Input lowercase sentence: ')
clientSocket.send(message.encode())
modifiedMessage = clientSocket.recv(1024).decode()
print('From Server: ', modifiedMessage)
clientSocket.close()
