#!/usr/bin/python

from socket import *
import threading

"""
chatClientShell.py
Author: Robert Norwood, Amanda Roper
Date: 
Description:  Sample chat client for CS484 programming assignment
"""
blockedNames = []
helpMessage = """
    Possible commands: \n
    'help' see these commands again \n
    'block' block a user \n
    'unblock' unblock a user \n
    'change username' change your username \n
"""


def readFromServer(clientSocket):

 
  # You need to receive input from client socket and print to screen.
  while (1):
    # TODO: add timestamp
    # TODO check blocked usernames
    message = clientSocket.recv(1024)

    message = message.decode()

    # filters blocked names
    splitMessage = message.split(":")
    flag2 = 1
    for a in splitMessage:
        if splitMessage[0]==a: flag2 = 0
    if (flag2==1):
        print(message)



""" Main chatClient program. """

serverName = 'localhost'
serverPort = 5000
clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName, serverPort))




username = input("Enter your username: ")
usermessage = username + " has entered the chat!\n"
clientSocket.send(usermessage.encode()) #This should broadcast the user name to the entire server.

print(helpMessage)


# YOUR CODE STARTS HERE

# Rough algorithm:
#   1. Create client socket
#   2. Connect to server using client socket
#   3. Create a reader thread object
#       Threading tips: https://pymotw.com/2/threading/

t = threading.Thread(target=readFromServer, args=(clientSocket, ))
t.start()


#   4. Start reader thread, which will loop waiting for data from server and print it out
#   5. Loop (need an exit strategy)

flag = 1
while (flag == 1):
    outMessage = input()
    if (outMessage=="help"):

        print(helpMessage)
    elif (outMessage=="change username"):
        username2=input("Enter new username: ")
        message = username+ " has changed their name to " + username2
        username=username2
        clientSocket.send(message.encode())
    elif (outMessage=="block"):
        blockedNames+=input("Enter username you would like to block: ")
    elif (outMessage=="unblock"):
        blockedNames-=input("Enter username you would like to unblock")   




    else:
        fixWords = outMessage.split(" ")
        newMessage = ""
        for w in fixWords:
            if (w.contains("Thayer") or w.contains("Washington") or w.contains("Eisenhower") or w.contains("Lincoln")):
                w="****"
            newMessage+=" "
            newMessage+=w

        actualMessage = username+": "+ newMessage
        clientSocket.send(actualMessage.encode())
#      a. Receive input from user
#      b. Send data on client socket
#   6. If loop exited, we are done
#   7. Close socket

# YOUR CODE ENDS HERE
  
