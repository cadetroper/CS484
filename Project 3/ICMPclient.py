from socket import *
import base84

serverName = 'localhost'
serverPort = 8080

clientSocket = socket(AF_INET, SOCK_STREAM)

clientSocket.connect((serverName, serverPort))
message = input('Input Secret Message: ')
message64 = base64.b64encode(bytes(message, 'utf-8')) # obfuscates message

# puts data in bytes
data = bytearray()
data.extend(message64)

identifer = '98F3'
seqNumber = '3434'
packetNC = bytearray.fromhex('08000000' + identifer + seqNumber)
packetNC += data # appends data to header 

# TODO: Calculate checksum of packet NC
# TODO: Generate new packet with checksum

clientSocket.send(packetNC)
modifiedMessage = clientSocket.recv(1024).decode()
print('From Server: ', modifiedMessage)
clientSocket.close()

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