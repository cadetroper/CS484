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
        parts = []
        parts = message.split(" ")
        lines = []
        lines = message.split("\n")

        #TODO store important parts that we need for processing flow, like file path, etc
        # Stores responses

        # gets current date to send with HTML response and formats
        # https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior
        curDate = datetime.strftime(datetime.today(),"%a, %d %b %Y %H:%M:%S %Z")

        # creating variable, setting later to actual file
        lastmod = "Tue, 18 Aug 2015 15:11:00"

        #CType placeholder, TODO: make it vary based on type of file requested
        acceptlangs = lines[6].split(" ")
        # cType = acceptlangs[1]
        cType = 'text/html'

        #https://emalsha.wordpress.com/2016/11/24/how-create-http-server-using-python-socket-part-ii/
        # "How to Create HTTP Server Using Python Socket Part II" Used to find out why files weren't rendering. Realized that we could use the file extention to set content type var. West Point, NY. 26 SEP 18.
        filename = lines[0].split(" ")[1]
        extn =  filename.split('.')[1]
        if (extn == "jpeg"): cType = 'image/jpg'
        elif (extn == "jpg"): cType = 'image/jpg'
        elif (extn=="css"): cType = 'text/css'


        #vars to sen
       
        #test line to see if it sends something
        # filename = "test1.html"


        data =""
        try:
            with (open(filename[1:], 'rb')) as f:
                data = f.read()
                # Last modified placeholder,Make it actually update. NOTE: CPT Chamberlain told me he doesn't care if we actually make the last modified work.
                htmlmessage="200 OK"

        except IOError as e:
            #this means that the file didn't exist
            movedinfo = open('moved').read()
            movedinfolines = movedinfo.split("\n")
            foundit = False
            htmlmessage = "\n\n\n\nIf this is still the message then it means that it did not execute the for or if statements on lines 54 & 59\n\n\n"
            for line in movedinfolines:
                if  filename[1:] in line:
                    #  TODO This only kinda works. MAybe we need to make it return a custom HTML 301 error to display? Try looking up for localhost:8080\values\default1.css. Should return not found (Based on my artificial moved file) but does something weird
                    htmlmessage = "301 Moved"
                    newlocation = line.split(" ")[1]
                    foundit = True
                if foundit == False:
                    htmlmessage = "404 Not Found:"

        length=len(data)


        okMSG = "HTTP/1.1 "+htmlmessage+" \r\nConnection: close" +"\r\nDate: " + curDate + "\r\nServer: Windows Python\r\nLast-Modified: " + lastmod + "\r\nContent-Length: " +str(length)
        if (htmlmessage=="301 Moved"): okMSG=okMSG+ "\r\nLocation:"+ newlocation
        okMSG=okMSG+ "\r\nContent-Type: " + cType + "\r\n\r\n"
        if(data!=""): finalData = bytearray(okMSG, 'utf-8')+data
        else: finalData =  bytearray(okMSG, 'utf-8')

    connectionSocket.send(finalData)
    connectionSocket.close()
