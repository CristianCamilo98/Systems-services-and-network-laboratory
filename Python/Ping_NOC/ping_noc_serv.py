import sys
import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
servAddr = ('localhost',int(sys.argv[1]))
sock.bind(servAddr)

while True:
    clientAddress = sock.recvfrom(10)
    print('Receive information from' + str(clientAddress[1][0]) +'/'+str(clientAddress[1][1]))
    sock.sendto(b'a',clientAddress[1])
