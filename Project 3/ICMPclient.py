from socket import *
import base64
import struct

serverName = '10.6.0.119'
serverPort = 8080


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

def sendSecret(message):
    clientSocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)


    clientSocket.connect((serverName, serverPort))

    message64 = base64.b64encode(message.encode()) # obfuscates message
    message = message64.decode()
    print(message)
    header = struct.pack("bbHHh", 8, 0, 0, 3, 1)
    print(header)
    csum = checksum(header + message.encode())

    newHeader = struct.pack("bbHHh", 8, 0, csum, 3, 1)



    # identifer = '\x98\xF3'
    # seqNumber = '\x34\x34'
    # packetNC = '\x08\x00\x00\x00' + identifer + seqNumber
    # packetNC = packetNC +  message64 # appends data to header 
    packetNC = newHeader + message.encode()  # appends data to header 
    # https://www.mkyong.com/python/python-3-convert-string-to-bytes/
    # rememinded to encode b84 string

    # csum = checksum(packetNC)
    # print(csum)
    # ssum = '{:x}'.format(csum)
    # print(ssum)

    # https://stackoverflow.com/questions/20905770/checksum-icmp-python-with-wireshark



    # TODO: Calculate checksum of packet NChttps://stackoverflow.com/questions/20247551/icmp-echo-checksum
    # essentially this involves splitting header and data into 16 bit words, getting the sum, 
    # then taking 1s complement. Insert this to checksum field. Can do using a loop through the 
    # Byte array, probably?

    # TODO: Generate new packet with checksum

    # finalPacket = '\x08\x00' + ssum + '\x33\x33' + seqNumber + message
  

    print(packetNC)
    clientSocket.send(packetNC)
    clientSocket.close()

while True:
  message = input('input secret message: ')
  sendSecret(message)

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