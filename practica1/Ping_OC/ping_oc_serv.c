#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<fcntl.h>
#include<unistd.h>

static const int MAXPENDING = 5;
void HandleTCPClient(int clntSocket);
int main(int argc, char *argv[])
{	

if(argc != 2){
	printf("Wrong amount of parameters <Server Port>\n");
	return 0;
}
in_port_t servPort = atoi(argv[1]); // atoi function converts an string into a binary number in this case the port that has been send throw the console 

// 1st create the TCP socket().



int servSock = socket(AF_INET,SOCK_STREAM,IPPROTO_TCP);
if(servSock < 0){
	printf("Socket() failed");
	return 0;
}
// "2nd" Is to construc the local address structure

struct sockaddr_in servAddr;
memset(&servAddr,0,sizeof(servAddr));
servAddr.sin_family=AF_INET;
servAddr.sin_port=htons(servPort);//htons checks that the format of the port is correct.
servAddr.sin_addr.s_addr=htonl(INADDR_ANY);// htonl() this function converts the "address" from host byter order to network byte order.

//"3rd" bind to the local address --> assign the socket an address with "bind()"


if(bind(servSock,(struct sockaddr*)&servAddr,sizeof(servAddr))<0){
	printf("bind() failed");
	return 0;
}
//"4th" Mark the socker for it to be hearing incoming connections with "listen()"

if(listen(servSock,MAXPENDING)<0){
	printf("listen() failed");
	return 0;
}
//"5th" Continuosly accept to get a new socket for each cliente connection and communicate with him using recv() & send() at the end close the connection with close()
for(;;){
struct sockaddr_in clntAddr;
socklen_t clntAddrLen =sizeof(clntAddr);
int clntSock = accept(servSock,(struct sockaddr*)&clntAddr,&clntAddrLen);
	if(clntSock<0){
		printf("accept() failed");
		return 0;
	}
// Now we will print the info of the client to check if is working properly
char clntName[INET_ADDRSTRLEN]; // String to save the client address
if(inet_ntop(AF_INET,&clntAddr.sin_addr.s_addr,clntName,sizeof(clntName))!=NULL)
	printf("Handling client %s/%d\n",clntName,ntohs(clntAddr.sin_port));
else
	printf("Unable to get client address");

HandleTCPClient(clntSock);

}
}

// FUNCTIONS
void HandleTCPClient(int clntSocket){
char buffer[BUFSIZ];

//receive message from client 
ssize_t numBytesRcvd = recv(clntSocket,buffer,BUFSIZ,0);
if(numBytesRcvd < 0){
	printf("recv() failed");
	return;
}
while(numBytesRcvd > 0){
	ssize_t numBytesSent = send(clntSocket,buffer,numBytesRcvd,0);
	if(numBytesSent < 0){
		printf("send()sent unexpected number of bytes");
		return;
	}
numBytesRcvd = recv(clntSocket,buffer,BUFSIZ,0);
if(numBytesRcvd < 0){
	printf("recv() failed");
	return;
}
}

close(clntSocket);
}

