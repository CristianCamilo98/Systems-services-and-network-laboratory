#CLIENTE
import socket, select, string, sys, pickle 


def prompt():
    sys.stdout.write('<' + name + '> ')
    sys.stdout.flush()

CONNECTION_LIST=[] #Here it will be save all the active users address and ports
CONNECTION_SOCKS = []
SEND_SOCKS = []
host = sys.argv[1]
port = int(sys.argv[2])
name = input("Introduce tu nombre de usuario: ")
#SERVER SOCKET & CONNECTION
server= socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket create for the server
server.connect((host,port)) #connected to the server
#USERS LISTENING SOCKET
user_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
user_sock.bind(("localhost",0))
user_sock.listen(10)
#SEND TO THE SERVER THE LISTENING PORT
address_sockuser = user_sock.getsockname()
server.sendall(pickle.dumps(address_sockuser))
#USER SOCKET TO CONNECT TO OTHERS

print("My socket listening is: [%s,%s]" %address_sockuser)

prompt() 

socket_list = [sys.stdin,server,user_sock]
while True:

    
    read_sockets, write_sockets, error_sockets = select.select(socket_list,[],[])
 #   read_sockets1, _,_ = select.select(user_sock,[],[])
    for sock in read_sockets:
        #CASE 1: SERVER SENDS ACTIVE USERS
        if sock == server: #Server will only send the clients connected to him 
            data = sock.recv(4096)    
            if not data:
                 print ('\nDisconnected from chat server')
                 sys.exit()
            else:
                CONNECTION_LIST = pickle.loads(data) #Address of sock of clients listening
                #CONNECTING TO THE REST OF CLIENTS
                for n in CONNECTION_LIST: 
                    if n != address_sockuser:
                        socketn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socketn.connect(n)
                        socket_list.append(socketn) 
                        SEND_SOCKS.append(socketn) #For broadcast
                prompt()
        #CASE 2: USERS CONNECT TO LISTENING SOCKETS
        elif sock == user_sock:
            sockfd, addr = user_sock.accept()   
            socket_list.append(sockfd)
            print(sockfd.getsockname())
            prompt()

        #CASE 3: WRITING
        elif sock == sys.stdin:   
            msg = sys.stdin.readline()
            msg ='<'+ name +'> ' + msg
            for n in SEND_SOCKS:
                    n.sendall(bytes(msg,'utf-8'))
        #CASE 4: REACIVING DATA 
        else:
            data=sock.recv(4096)
            if not data:
                print('\nDisconnected from chat server')
                sock.close()
                sys.exit()
            else:
                sys.stdout.write(data.decode('utf-8'))
        
