#CLIENTE
import socket, select, string, sys, pickle 


def prompt():
    sys.stdout.write('<' + name + '> ')
    sys.stdout.flush()


host = sys.argv[1]
port = int(sys.argv[2])
name = input("Introduce tu nombre de usuario: ")
s= socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host,port))
prompt() 
while True:
    socket_list = [sys.stdin,s]
    
    read_sockets, write_sockets, error_sockets = select.select(socket_list,[],[])

    for sock in read_sockets:
        if sock == s:
            data = sock.recv(4096)
            if not data:
                 print ('\nDisconnected from chat server')
                 sys.exit()
            else:
                sys.stdout.write(data.decode('utf-8'))
                prompt() 

        
        else:
            msg = sys.stdin.readline()
            msg ='<'+ name +'> ' + msg
            s.sendall(bytes(msg,'utf-8'))
            prompt()
