from socket import *
from datetime import *
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))
serverSocket.listen(1)

print("The server is ready to receive")

while True:
    connectionSocket, addr = serverSocket.accept()
    message = connectionSocket.recv(1024).decode()
    if message[0:3]=="GET":
	    print(message)
	    parts = []
	    parts = message.split(" ")
	    lines = []
	    lines = message.split("\n")

	    #TODO store important parts that we need for processing flow, like file path, etc
	    #print(parts[1]+parts[3])
	    # Stores responses
		# this print only has / and localhost:8080 because it doesn't see the \n as a space. 

	    #Placeholder data. TODO: Make it read a file
	    #with open('test1.html') as f:
	    #	data = f.read()
		#moving all of this down.


	    # gets current date to send with HTML response and formats
	    curDate = datetime.strftime(datetime.today(),"%a, %d %b %Y %H:%M:%S %Z")

	    # Last modified placeholder, TODO: Make it actually update
	    lastmod = "Tue, 18 Aug 2015 15:11:00"

	    #CType placeholder, TODO: make it vary based on type of file requested
	    acceptlangs = lines[6].split(" ")
	    cType = acceptlangs[1]

	    length=len(data)
	    #vars to send
        filename = lines[0].split(" ")[1]
	    try:
	        with (open(filename)) as f:
	            data = f.read()

	    except IOError as e:
	        #this means that the file didn't exist
	        movedinfo = open('moved.txt').read()
	        movedinfolines = movedinfo.split("\n")
	        foundit = False
	        htmlmessage = "\n\n\n\nIf this is still the message then it means that it did not execute the for or if statements on lines 54 & 59\n\n\n"
	        for line in movedinfolines:
	            if line.contains(filename):
	                htmlmessage = "301 Moved"
		            newlocation = line.split(" ")[1]
	                foundit = True
	            if foundit = False:
	            htmlmessage = "404 Not Found:

	    # Consolidates message. TODO: make a few shorter lines insead of this one big line. TODO: Have options for 404 and 301 status errors
	    okMSG = "HTTP/1.1 "+htmlmessage+"<cr><lf>Date: " + curDate + "<cr><lf>\nServer: Windows Python <cr><lf>\nLast-Modified: " + lastmod + "<cr><lf>\nContent-Length: " +str(length) + "<cr><lf>\nContent-Type: " + cType + "<cr><lf><cr><lf>" + data 
    print(okMSG)
    connectionSocket.send(okMSG.encode())
    connectionSocket.close()
