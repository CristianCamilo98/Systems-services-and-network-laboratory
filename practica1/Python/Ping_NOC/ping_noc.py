import socket
import sys
import time

sock = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

server_address = (sys.argv[1],int(sys.argv[2]))

number_pings = int(sys.argv[3])
message = b'Hello'

print('PING ' + str(sys.argv[1]) +' (' + str(sys.argv[1]) + ') 56(84) bytes of data.')
while number_pings != 0:
    sock.sendto(message, server_address)
    response = sock.recvfrom(5)
    print('ping Received '+ str(response[1][0])+'/'+str(response[1][1]))
    number_pings=number_pings-1
    time.sleep(1)

sock.close()
