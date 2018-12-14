from socket import *
import base64
import threading
import sys
import struct

serverName = 'localhost'
serverPort = 8080
serverSocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)
serverSocket.bind(('', serverPort))

# https://stackoverflow.com/questions/20905770/checksum-icmp-python-with-wireshark
# # def carry_around_add(a,b):
#   c = a + b
#   return (c & 0xffff) + (c>>16)

seqNumber = 4
idn = 45
def checksum(msg):
  # headersum = bin(8 << 4) + bin(seqNumber) + bin(idn)
  headersum = 0

  for i in range(0, len(msg), 2):
    w = msg[i]+ (msg[i+1]<< 8)
    # headersum = carry_around_add(headersum, w)
    headersum = headersum + w
  headersum = headersum + (headersum >> 16)
  headersum =  ~headersum & 0xffff
  return headersum
    

def readFromServer(clientSocket, stop_event):
  while (not stop_event.is_set()):
    request, addr = serverSocket.recvfrom(1024)

    data = request[10:]
    message = base64.b64decode(data)

    print(message.decode())
      


clientSocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

clientSocket.connect((serverName, serverPort))

kill = threading.Event()

t = threading.Thread(target=readFromServer, args=(clientSocket,kill, ))
t.start()


while True:
  serverName = "localhost"
  serverPOrt = 8080
  
  message = input('input secret message: ')

  message64 = base64.b64encode(message.encode()) # obfuscates message
  message = message64.decode()

  header = struct.pack("bbHHh", 8, 0, 0, 3, 1)
 
  csum = checksum(header + message.encode())

  newHeader = struct.pack("bbHHh", 8, 0, csum, 3, 1)

  packetNC = newHeader + message.encode()  # appends data to header 
  # https://www.mkyong.com/python/python-3-convert-string-to-bytes/
  # https://stackoverflow.com/questions/20905770/checksum-icmp-python-with-wireshark

  clientSocket.send(packetNC)
#  clientSocket.close()

# What ICMP Packet looks like https://stackoverflow.com/questions/34614893/how-is-an-icmp-packet-constructed-in-python
   # 0                   1                   2                   3
   # 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
   # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   # |     Type(8)   |     Code(0)   |          Checksum             |
   # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   # |           Identifier          |        Sequence Number        |
   # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
   # |                             Payload                           |
   # +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+

  # From sample downloaded from wiresharks website (in github folder for reference)
  # we need type 8 code 0
 # Which is hex  08 for type and 00 for code. We'll just use our own process identifer
 # and sequence number. Checksum, identifier, and sequence are each two bytes. 
 # Total header size is 8 bytes. 

 # how to calculate ICMP checksum: https://osqa-ask.wireshark.org/questions/11061/icmp-checksum

 # 