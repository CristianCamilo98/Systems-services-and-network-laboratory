import sys
import socket
import time

numberPings = int(sys.argv[3])
sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servAddress=(str(sys.argv[1]),int(sys.argv[2]))
message = b'Hello'
sock.connect(servAddress)

print('PING ' + str(sys.argv[1]) +' (' + str(sys.argv[1]) + ') 56(84) bytes of data.')
while numberPings!=0: 
    sock.sendall(message)
    recvAddr = sock.recv(32)
    numberPings = numberPings - 1
    print('Ping received ' + socket.gethostbyname(servAddress[0])+ '/' + str(servAddress[1]))
    time.sleep(1)
sock.close()

