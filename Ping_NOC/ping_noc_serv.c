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

int main(int argc, char *argv[])
{	

if(argc != 2){
	printf("Wrong amount of parameters <Server Port>\n");
	return 0;
}
in_port_t servPort = atoi(argv[1]); // atoi function converts an string into a binary number in this case the port that has been send throw the console 
char buffer[1]="a";
size_t lenbuffer = sizeof(buffer);
// 1st create the UDP socket().

int servSock = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP);
if(servSock < 0){
	printf("Socket() failed");
	return 0;
}
// "2nd" Is to construc the local address structure

struct sockaddr_in servAddr;
socklen_t servAddrLen=sizeof(servAddr);
memset(&servAddr,0,sizeof(servAddr));
servAddr.sin_family=AF_INET;
servAddr.sin_port=htons(servPort);//htons checks that the format of the port is correct.
servAddr.sin_addr.s_addr=htonl(INADDR_ANY);// htonl() this function converts the "address" from host byter order to network byte order.

//"3rd" bind to the local address --> assign the socket an address with "bind()"


if(bind(servSock,(struct sockaddr*)&servAddr,servAddrLen)<0){
	printf("bind() failed");
	return 0;
}


//"4th" Continuosly accept to get a new socket for each cliente connection and communicate with him using recv() & send() at the end close the connection with close()
for(;;){
// RECEIVING INFORMATION 	
struct sockaddr_in  clntAddr;
socklen_t clntAddrLen = sizeof(clntAddr);

ssize_t recvBytes = recvfrom(servSock,buffer,lenbuffer,0,(struct sockaddr *)&clntAddr,&clntAddrLen);
if(recvBytes < 0){
	printf("Error at recvfrom()");
	return 0;
}
char clntName[INET_ADDRSTRLEN];
if(inet_ntop(AF_INET,&clntAddr.sin_addr.s_addr,clntName,sizeof(clntName)) == NULL)
	return 0;

printf("Receive information from %s/%d\n",clntName,ntohs(clntAddr.sin_port));

ssize_t numBytesSent = sendto(servSock,buffer,lenbuffer,0,(struct sockaddr *)&clntAddr,clntAddrLen);


}
close(servSock);
return 0;
}
