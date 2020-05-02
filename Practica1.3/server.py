import sys
import socket
import select
import time
import threading
import os
import pickle
from wsgiref.handlers import format_date_time
from datetime import datetime
from time import mktime

args = len(sys.argv)
BUFFER = 4096
entradas = []
salidas = []
errores = {}
timeout = 300

if args != 2:
    print("Wrong, the parameter must be: <Port>")
else:
    puerto = int(sys.argv[1])
    if puerto <= 1024:
        print("El puerto debe ser mayor que 1024\n")
        sys.exit()
    print("Server started on port "+str(puerto))
    my_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  #Creacion del socket
    my_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)  #Nos permite cambiar el tamanyo del buffer 
    my_sock.bind(('',puerto))           #Asociacion del socket
    my_sock.listen(10)                  #Crea cola de escucha
    entradas.append(my_sock)            #Agrega el socket creado a la lista de entrada

    while True:
        lecturas, escrituras,excepciones = select.select(entradas,salidas,errores,timeout)
        if not (lecturas or escrituras or excepciones):
            now = datetime.now()
            stamp = mktime(now.timetuple())
            print("Servidor inactivo:",format_date_time(stamp))
        for client_sock in lecturas:
            if client_sock == my_sock:
                sockfd, addr = my_sock.accept()
                entradas.append(sockfd)
                print("Cliente (%s,%s) conectado " %addr)
            else:
                respuesta = "{}\r\nDate: {}\r\nServer: practica_uah\r\nContent-type: {}\r\nContent-length: {}\r\nConnection: {}\r\n\r\n"
                data = client_sock.recv(BUFFER)
                if not data:
                    entradas.remove(client_sock)
                    client_sock.close()
                else:
                    now = datetime.now()
                    stamp = mktime(now.timetuple())
                    data = data.decode("utf-8") #Convertimos los bytes en string
                    data = data.split("\r\n") # Lo separamos en lineas
                    version = data[0].split()
                    version = version[2]
                    
                    data = data[0].split() # Separamos cada palabra de la primera linea de las cabeceras HTTP
                    metodo = data[0]
                    peticion ="."+ data[1]
                    content_type = data[1].split(".")
                    content_type = content_type[1]
                    if metodo == "GET":
                        try:
                            if version == "HTTP/1.1" or version == "HTTP/1.0":
                                connection = "close"
                                f = open(peticion,"rb")
                                file_stats = os.stat(peticion)
                                data = f.read()
                                f.close()
                                if version == "HTTP/1.1":
                                    connection = "keep-alive"
                                if content_type == "html":
                                    content_type = "text/html"
                                elif content_type == "jpg":
                                    content_type = "image/jpg"
                                    connection = "close"
                                else:
                                    content_type ="bytes"
                                respuesta = respuesta.format(version+" "+"200 OK",format_date_time(stamp),content_type,str(file_stats.st_size),connection)
                                respuesta = bytes(respuesta,'utf-8')
                                respuesta = respuesta + data
                                client_sock.sendall(respuesta)
                                if version == "HTTP/1.0":
                                    entradas.remove(client_sock)
                                    client_sock.close()
                            else:
                                mensaje = bytes("Metodo no permitido","utf-8")
                                respuesta = bytes(respuesta.format(version+" "+"405 Method Not allowed",format_date_time(stamp),"text/plain",len(mensaje),cmnnection),"utf-8")
                                respuesta += mensaje
                                client_sock.sendall(respuesta)
                                entradas.remove(client_sock)
                                
                        except FileNotFoundError:
                            mensaje =bytes("Pagina no encontrada","utf-8")
                            respuesta =bytes(respuesta.format(version+" "+"404 Not Found",format_date_time(stamp),"text/plain",len(mensaje),connection),"utf-8")
                            respuesta += mensaje
                            client_sock.sendall(respuesta)
                            entradas.remove(client_sock)
                            print("file not found")

