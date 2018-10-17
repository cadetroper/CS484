#!/usr/bin/python

from socket import *
import threading

"""
chatClientShell.py
Author: Robert Norwood, Amanda Roper
Date: 
Description:  Sample chat client for CS484 programming assignment
"""

def readFromServer(clientSocket):

 
  # You need to receive input from client socket and print to screen.
  while (1):
	message = clientSocket.recv(1024)
	message = message.decode()
	print(message)



""" Main chatClient program. """

serverName = 'localhost'
serverPort = 9000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))




username = input("Enter your username: ")
usermessage = username + " has entered the chat!\n"
send(usermessage.encode()) #This should broadcast the user name to the entire server.



# YOUR CODE STARTS HERE

# Rough algorithm:
#   1. Create client socket
#   2. Connect to server using client socket
#   3. Create a reader thread object
#	 	Threading tips: https://pymotw.com/2/threading/

t = threading.Thread(target=readFromServer, args=(clientSocket, ))
t.start()


#   4. Start reader thread, which will loop waiting for data from server and print it out
#   5. Loop (need an exit strategy)
#      a. Receive input from user
#      b. Send data on client socket
#   6. If loop exited, we are done
#   7. Close socket

# YOUR CODE ENDS HERE
  
