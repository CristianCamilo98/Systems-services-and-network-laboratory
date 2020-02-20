all: server user

server: ping_noc_serv.o 
	cc ping_noc_serv.o -o server

user: ping_noc.o
	cc ping_noc.o -o user

ping_noc.o: ping_noc.c
	cc -c ping_noc.c

ping_noc_serv.o: ping_noc_serv.c
	cc -c ping_noc_serv.c

clean:
	rm server
	rm user
	rm *.o
