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

	    #TODO store important parts that we need for processing flow, like file path, etc
	    print(parts[1]+parts[3])
	    # Stores responses

	    #Placeholder data. TODO: Make it read a file
	    with open('test1.html') as f:
	    	data = f.read()
		


	    # gets current date to send with HTML response and formats
	    curDate = datetime.strftime(datetime.today(),"%a, %d %b %Y %H:%M:%S %Z")

	    # Last modified placeholder, TODO: Make it actually update
	    lastmod = "Tue, 18 Aug 2015 15:11:00"

	    #CType placeholder, TODO: make it vary based on type of file requested
	    cType = "text/html"

	    length=len(data)
	    #vars to send

	    # Consolidates message. TODO: make a few shorter lines insead of this one big line. TODO: Have options for 404 and 301 status errors
	    okMSG = "HTTP/1.1 200 OK<cr><lf>Date: " + curDate + "<cr><lf>Server: Windows Python <cr><lf>Last-Modified: " + lastmod + "<cr><lf>Content-Length: " +str(length) + "<cr><lf>Content-Type: " + cType + "<cr><lf><cr><lf>" + data 
    print(okMSG)
    connectionSocket.send(okMSG.encode())
    connectionSocket.close()
