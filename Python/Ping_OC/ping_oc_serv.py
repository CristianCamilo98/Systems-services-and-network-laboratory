import sys
import socket

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
servAddr = ('localhost',int(sys.argv[1]))
message =b'Hello'
sock.bind(servAddr)

sock.listen(10)
sockoc, addr = sock.accept()
print('Handling Client' + str(addr))
while True:
    data = sockoc.recv(32)
    if not data:
        break
    sockoc.sendall(message)
sock.close()
