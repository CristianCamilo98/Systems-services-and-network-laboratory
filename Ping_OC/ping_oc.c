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

/*Creating the socket in this case TCP socket*/

int sock = socket(AF_INET, SOCK_STREAM,IPPROTO_TCP);
if(sock < 0)
	printf("Error al crear el socket()\n");
/*Creating the server address structure*/
struct sockaddr_in servAddr;  // the sockaddr_in is a structure created to be a container for the information of IP and port to connect to
memset(&servAddr,0,sizeof(servAddr)); //Using the function memset the structure is initialized

/*Filling the structure servAddr created before*/
servAddr.sin_family=AF_INET; // Internet protocol thats why its assign "AF_INET"(IPv4)
servAddr.sin_addr.s_addr=address->s_addr; //Assigning the IP address to the server address structure
servAddr.sin_port = htons(servPort);//this functions checks that the binary value is formated as require by the API

/*Stablishing the connection to the socket addressed in "servAddr" with the function connect()*/
if(connect(sock,(struct sockaddr *)&servAddr,sizeof(servAddr))<0){	
	   printf("connect() failed\n");
	   return 0;
}
char message[]="a";
size_t length = strlen(message);// in "length" its saved the length of the message

/*Sending the "Message"*/

char clntName[INET_ADDRSTRLEN];
if(inet_ntop(AF_INET,&servAddr.sin_addr.s_addr,clntName,sizeof(clntName)) == NULL)
	return 0;
printf("PING %s (%s) 56(84) bytes of data.\n",clntName,clntName);

while(numberpings!=0){
ssize_t numBytes = send(sock,message,length,0);
if(numBytes<-1){
	printf("Unexpected amount of data sent");
	return 0;
	}
ssize_t numBytesrcv = recv(sock,buffer,1,0);
if(numBytesrcv <= 0){
printf("recv() failed or connection closed prematurely");
}else if(numBytesrcv==1){
printf("ping receive\n");
numberpings--;
sleep(1);
numBytesrcv=0;//resseting the numBytesrecv
}else{
printf("RUUUUN!");
return 0;
}

}


close(sock);
exit(0);
}

