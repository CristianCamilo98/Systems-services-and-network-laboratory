#CLIENTE
import socket, select, string, sys, pickle 


def prompt():
    sys.stdout.write('<' + name + '> ')
    sys.stdout.flush()

CONNECTION_LIST=[] #Here it will be save all the active users address and ports
CONNECTION_SOCKS = []
host = sys.argv[1]
port = int(sys.argv[2])
name = input("Introduce tu nombre de usuario: ")
#SERVER SOCKET
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket create for the server
server.connect((host,port)) #connected to the server
#USERS LISTENING SOCKET
user_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_sock.bind(("localhost",0))
user_sock.listen(10)
address_sockuser = user_sock.getsockname()
server.sendall(pickle.dumps(address_sockuser))


prompt() 

while True:
    socket_list = [sys.stdin,server,user_sock]
    
    read_sockets, write_sockets, error_sockets = select.select(socket_list,[],[])

    for sock in read_sockets:
        #CASE 1: SERVER SENDS ACTIVE USERS
        if sock == server: #Server will only send the clients connected to him 
            data = sock.recv(4096)    
            if not data:
                 print ('\nDisconnected from chat server')
                 sys.exit()
            else:
                CONNECTION_LIST = pickle.loads(data) #Address of sock of clients listening
                print(CONNECTION_LIST)
                for n in CONNECTION_LIST:    
                    try:
                        user_sock.connect(n)
                    except:
                        print("already connected to:")
                        print(n)
                prompt()

        #CASE 2: USERS CONNECT
        elif sock == user_sock:
            sockfd, addr = user_sock.accept()   
            print("connection accepted")
            socket_list.append(sockfd)
            print("connected to (%s,%s)." %addr)


        #CASE 3: WRITING
        elif sock == sys.stdin:   
            msg = sys.stdin.readline()
            msg ='<'+ name +'> ' + msg
            for n in CONNECTION_SOCKS:
                try:
                    n.sendall(bytes(msg,'utf-8'))
                    print("sending data")
                except:
                    print("Error at sending data")
            prompt()
        #CASE 4: REACIVING DATA 
        else:
            data=sock.recv(4096)
            if not data:
                print('\nDisconnected from chat server')
                sys.exit
            else:
                sys.stdout.write(data.decode('utf-8'))
                print("hey")
                prompt()
        
