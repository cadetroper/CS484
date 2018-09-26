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
        print(parts)

        #TODO store important parts that we need for processing flow, like file path, etc
        # Stores responses

        # gets current date to send with HTML response and formats
        curDate = datetime.strftime(datetime.today(),"%a, %d %b %Y %H:%M:%S %Z")

        # creating variable, setting later to actual file
        lastmod = "Tue, 18 Aug 2015 15:11:00"

        #CType placeholder, TODO: make it vary based on type of file requested
        acceptlangs = lines[6].split(" ")
        # cType = acceptlangs[1]
        cType = 'text/html' #https://emalsha.wordpress.com/2016/11/24/how-create-http-server-using-python-socket-part-ii/
        extn =  parts[1].split('.')[1]
        if (extn == "jpeg"): cType = 'image/jpg'
        elif (extn == "jpg"): cType = 'image/jpg'
        elif (extn=="css"): cType = 'text/css'


        #vars to sen
        filename = lines[0].split(" ")[1]
        print(filename)
        #test line to see if it sends something
        # filename = "test1.html"


        data =""
        try:
            with (open(filename[1:], 'rb')) as f:
                data = f.read()
                # Last modified placeholder, TODO: Make it actually update
                # SOURCE: https://stackoverflow.com/questions/39359245/from-stat-st-mtime-to-datetimef
                # filestat = datetime.fromtimestamp(path.getmtime(filename))
                htmlmessage="200 OK"

        except IOError as e:
            #this means that the file didn't exist
            movedinfo = open('moved').read()
            movedinfolines = movedinfo.split("\n")
            foundit = False
            htmlmessage = "\n\n\n\nIf this is still the message then it means that it did not execute the for or if statements on lines 54 & 59\n\n\n"
            for line in movedinfolines:
                if  filename in line:
                    htmlmessage = "301 Moved"
                    newlocation = line.split(" ")[1]
                    foundit = True
                if foundit == False:
                    htmlmessage = "404 Not Found:"

        length=len(data)

        # Consolidates message. TODO: make a few shorter lines insead of this one big line. 
        # okMSG = "HTTP/1.1 "+htmlmessage+"\n<cr><lf>Date: " + curDate + "<cr><lf>\nServer: Windows Python<cr><lf>\nLast-Modified: " + lastmod + "<cr><lf>\nContent-Length: " +str(length) + "<cr><lf>\nContent-Type: " + cType + "<cr><lf><cr><lf>" + data 
        okMSG = "HTTP/1.1 "+htmlmessage+"\r\nDate: " + curDate + "\r\nServer: Windows Python\r\nLast-Modified: " + lastmod + "<cr><lf>Content-Length: " +str(length) + "\r\nContent-Type: " + cType + "\r\n\r\n"
        finalData = bytearray(okMSG, 'utf-8')+data
    print(okMSG)
    connectionSocket.send(finalData)
    connectionSocket.close()
