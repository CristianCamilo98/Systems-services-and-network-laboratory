#SERVER
import socket, select, pickle

def broadcast_data (sock,message):
    for socket in CONNECTION_LIST: #It will go through all the active sockets and it will send the data.
        if socket != server_socket :# it will not send the data to the server and itself
            try :
                socket.sendall(message)
            except :
                socket.close()
                CONNECTION_LIST.remove(socket)



CONNECTION_LIST = []  #Here the id of the sockets will be saved.
ADDRESS_USERS = [] #Here the address will be saved.
RECV_BUFFER = 4096
PORT = 5001


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
server_socket.bind(("localhost",PORT))
server_socket.listen(10)
CONNECTION_LIST.append(server_socket) 

print ("chat serverr started on port " + str(PORT))

while True:
       
    read_sockets,write_sockets,error_sockets = select.select(CONNECTION_LIST,[],[])
#In read_sockets it will be store all the sockets and once they are readible it will jump to the next line
    for sock in read_sockets:
        if sock == server_socket:# Handle the first connection 
            sockfd, addr = server_socket.accept()
            CONNECTION_LIST.append(sockfd)
            print ("client (%s,%s) connected " %addr)
            

        else:
            data = sock.recv(RECV_BUFFER)
            if data:
                ADDRESS_USERS.append(pickle.loads(data))       
                broadcast_data(sockfd,pickle.dumps(ADDRESS_USERS))
                print(ADDRESS_USERS)
            else:
                
               # broadcast_data(sock,"client (%s,%s) is offline \n" %addr)
                print ("Client (%s,%s) is offline" %addr)
                CONNECTION_LIST.remove(sock)
                sock.close()

                
server_socket.close()
