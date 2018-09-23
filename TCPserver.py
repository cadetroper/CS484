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
        # Stores responses

        # gets current date to send with HTML response and formats
        curDate = datetime.strftime(datetime.today(),"%a, %d %b %Y %H:%M:%S %Z")

        # creating variable, setting later to actual file
        lastmod = "Tue, 18 Aug 2015 15:11:00"

        #CType placeholder, TODO: make it vary based on type of file requested
        acceptlangs = lines[6].split(" ")
        cType = acceptlangs[1]


        #vars to sen
        filename = lines[0].split(" ")[1]

        try:
            with (open(filename)) as f:
                data = f.read()
                # Last modified placeholder, TODO: Make it actually update
                # SOURCE: https://stackoverflow.com/questions/39359245/from-stat-st-mtime-to-datetimef
                filestat = datetime.datetime.fromtimestamp(path.getmtime(filename))

        except IOError as e:
            #this means that the file didn't exist
            movedinfo = open('moved').read()
            movedinfolines = movedinfo.split("\n")
            foundit = False
            htmlmessage = "\n\n\n\nIf this is still the message then it means that it did not execute the for or if statements on lines 54 & 59\n\n\n"
            for line in movedinfolines:
                if not filename in line:
                    htmlmessage = "301 Moved"
                    newlocation = line.split(" ")[1]
                    foundit = True
                if foundit == False:
                    htmlmessage = "404 Not Found:"

        length=len(data)

        # Consolidates message. TODO: make a few shorter lines insead of this one big line. 
        okMSG = "HTTP/1.1 "+htmlmessage+"<cr><lf>Date: " + curDate + "<cr><lf>\nServer: Windows Python <cr><lf>\nLast-Modified: " + lastmod + "<cr><lf>\nContent-Length: " +str(length) + "<cr><lf>\nContent-Type: " + cType + "<cr><lf><cr><lf>" + data 
    print(okMSG)
    connectionSocket.send(okMSG.encode())
    connectionSocket.close()
