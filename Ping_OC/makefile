all: user server

user: ping_oc.o
	cc ping_oc.o -o user

server: ping_oc_serv.o
	cc ping_oc_serv.o -o server

ping_oc_serv.o: ping_oc_serv.c
	cc -c ping_oc_serv.c

ping_oc.o: ping_oc.c
	cc -c ping_oc.c

clean:
	rm user
	rm server
	rm *.o
