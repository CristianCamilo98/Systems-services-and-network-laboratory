#include<stdio.h>
#include<stdlib.h>
#include<string.h>
#include<unistd.h>
#include<sys/types.h>
#include<sys/socket.h>
#include<netinet/in.h>
#include<arpa/inet.h>
#include<netdb.h>



int main(int argc, char *argv[])
{
	/*First of all it needs to be checked that is been passed the right amount of arguments*/
if(argc != 4){
	printf("Wrong number of parameters. Structure -> <Server Address> <Server Port> [<Number of pings>]\n");
	return 0;
	}	
struct hostent *DNS_resolution;
struct in_addr *address;
char buffer[1];

DNS_resolution = gethostbyname(argv[1]);
if(DNS_resolution==NULL){
printf("Theres been an error with the DNS resolution\n");
return 0;
}

address=(struct in_addr *)(DNS_resolution->h_addr);
in_port_t servPort=atoi(argv[2]);  
int numberpings=atoi(argv[3]);

//Creating the UDP socket

int sock = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP);
if(sock<0){
	printf("Error at creating socket()");
	return 0;
}
//Creating the server address structure.
struct sockaddr_in servAddr;
memset(&servAddr,0,sizeof(servAddr));

//Filling the structure sockaddr_in of the server to reach
servAddr.sin_family=AF_INET;
servAddr.sin_port=htons(servPort);
servAddr.sin_addr.s_addr=address->s_addr;

char message[]="b";
size_t length = strlen(message);
socklen_t addrlen = sizeof(servAddr);

//Structure at which is going to be saved the information of the servsock
char clntName[INET_ADDRSTRLEN];
if(inet_ntop(AF_INET,&servAddr.sin_addr.s_addr,clntName,sizeof(clntName)) == NULL)
	return 0;
printf("PING %s (%s) 56(84) bytes of data.\n",clntName,clntName);
while(numberpings!=0){
ssize_t sentBytes = sendto(sock,message,length,0,(struct sockaddr *)&servAddr,addrlen);
if(sentBytes != 1){
printf("Error at sendto()\n");
return 0;
}
char buffer[0];
ssize_t rcvBytes = recvfrom(sock,buffer,1,0,0,0);
if(rcvBytes !=1 ){
printf("Amount of data not expected");
return 0;
}
printf("Ping received \n");
sleep(1);
numberpings--;
}
}
