#!/usr/bin/python

from socket import *
import threading
from datetime import *
import sys

"""
chatClientShell.py
Author: Robert Norwood, Amanda Roper
Date: 
Description:  Sample chat client for CS484 programming assignment
"""
blockedNames = []
helpMessage = """
    Possible commands: \n
    #user <handle>: changes a user handle\n
    #block <user>: blocks this user's message\n
    #unblock <user>: unblocks this user's message\n
    #help: shows this screen\n
    #bye: quits chat program\n
"""


def readFromServer(clientSocket):

 
  # You need to receive input from client socket and print to screen.
  while (1):
    # TODO: add timestamp
    # TODO check blocked usernames
    message = clientSocket.recv(1024)
    print(blockedNames)

    message = message.decode()
    curDate = datetime.strftime(datetime.today(),"%a, %d %b %Y %H:%M:%S %Z")

    # filters blocked names
    splitMessage = message.split(":")
    flag2 = 1
    for a in blockedNames:
        if (splitMessage[0]==a): flag2 = 0
    if (flag2==1):
        print(curDate + message)



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
    if (outMessage[:5]=="#help"):
        print(outMessage[:5])
        print(helpMessage)
    elif (outMessage[:5]=="#user"):
        username2=outMessage[6:]
        message = username+ " has changed their name to " + username2
        username=username2
        clientSocket.send(message.encode())
    elif (outMessage[:6]=="#block"):
        print(outMessage[7:])
        c = ""
        blockedNames+=c.join(outMessage[7:])
    elif (outMessage[:7]=="#unblock"):
        c = ""
        blockedNames-=c.join(outMessage[8:])
    elif (outMessage[:4]=="#bye"):
        message = username+" has left the chat."
        clientSocket.send(message.encode())
        sys.exit()
        # TODO Quit only kind of kills the program. Need something besides exit.



    else:
        fixWords = outMessage.split(" ")
        newMessage = ""
        for w in fixWords:
            a = w.lower()
            if ("thayer" in a or "washington" in a or "eisenhower" in a or "lincoln" in a):
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
  
