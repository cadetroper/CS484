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
blockedNames = list()
helpMessage = """
    Possible commands: \n
    #user <handle>: changes a user handle\n
    #block <user>: blocks this user's message\n
    #unblock <user>: unblocks this user's message\n
    #help: shows this screen\n
    #bye: quits chat program\n
"""


def readFromServer(clientSocket, stop_event):

 
  # You need to receive input from client socket and print to screen.
  while (not stop_event.is_set()):
    # TODO: add timestamp
    # TODO check blocked usernames
    message = clientSocket.recv(1024)

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
kill = threading.Event()
# https://stackoverflow.com/questions/18018033/how-to-stop-a-looping-thread-in-python
# Used to figure out how to use an event to stop the receving thread. West Point, NY. 31 OCT 18

t = threading.Thread(target=readFromServer, args=(clientSocket,kill, ))
t.start()


#   4. Start reader thread, which will loop waiting for data from server and print it out
#   5. Loop (need an exit strategy)

flag = 1
while (flag == 1):
    outMessage = input()
    if (outMessage[:5]=="#help"):
        print(helpMessage)
    elif (outMessage[:5]=="#user"):
        username2=outMessage[6:]
        message = username+ " has changed their name to " + username2
        username=username2
        clientSocket.send(message.encode())
    elif (outMessage[:6]=="#block"):
        print(outMessage[7:] + " has been blocked")
        c = ""
        # https://www.dotnetperls.com/string-list-python
        # used to realize I need to use .append not += otherwise it screws thigns up
        blockedNames.append(outMessage[7:])
    elif (outMessage[:8]=="#unblock"):
        print (outMessage[9:]+ " has been removed from blocklist")
        blockedNames.remove(outMessage[9:])
        #TODO this doesn't actually remove the name from the blocklist
    elif (outMessage[:4]=="#bye"):
        message = username+" has left the chat."
        clientSocket.send(message.encode())
        kill.set()
        t.join()
        flag = 0
        exit()
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
  
