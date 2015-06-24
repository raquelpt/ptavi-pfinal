#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

import sys
import SocketServer
import os
import os.path
import socket
import time


class Proxy(SocketServer.DatagramRequestHandler):

    def register2file(self):
        """
        Listado con los usuarios registrados en cada momento.
        """

        fich = open(PATH_DATABASE, "w")
        escribe = User + "\t" + IP + "\t" + Port + "\t"
        escribe += Date + "\t" + Expires + "\r\n"
        fich.write(escribe)
        for clave in registro:
            tiempo = time.gmtime(float(registro[clave][3]))
            hora = time.strftime("%Y%m%d%H%M%S", tiempo)
            fich.write(linea)
        fich.close()

    def handle(self):

        while 1:
            line = self.rfile.read()
            if not line:
                break
            Metodo = line.split(" ")[0]
            Linea = line.split(" ")

            if Metodo == "Bad_Request":
                print "SIP/2.0 400 Bad Request" + "\r\n\r\n"
                self.wfile.write("SIP/2.0 400 Bad Request" + "\r\n\r\n")
            elif Metodo == "INVITE":
                print line
                Destinatario = Linea[2]
                self.Send()
                if Booleano == True:
                       continue
            elif Metodo == "ACK":
                Destinatarios = line.split(":")[1]
                Destinatario = Destinatarios.split(" ")[0]
                print line
                self.Send()
                if Booleano == True:
                       continue

            elif Metodo == "BYE":
                    print line
                    Destinatario1 = Linea[1]
                    Destinatario = Destinatario1.split(":")[1]
                    self.Send()
                    if Booleano == True:
                        continue
            elif Metodo == "REGISTER":
                print line
                direccion = Linea[1].split(":")[1]
                expires = int(Linea[4])
                if expires == "0":
                    fich.write(str(time.time()) + " Finishing" + "\r\n")
                    fich.close()
                else:
                    fich.write(str(time.time()) + " Starting..." + "\r\n")
                    fich.write(str(time.time()) + " Register " + \
                    direccion + "\r\n")
                    puerto = int(Linea[1].split(":")[2])
                    timenow = time.time()
                    timeandexp = timenow + expires
                    Ip = "127.0.0.1"
                    valores = [Ip, puerto, timenow, timeandexp]
                    dicc[direccion] = valores
                    print "SIP/2.0 200 OK" + "\r\n\r\n"
                    self.wfile.write("SIP/2.0 200 OK" + "\r\n\r\n")
                    self.register2file()
                    for direccion in dicc.keys():
                           if timenow >= dicc[direccion][3]:
                               del dicc[direccion]
                               print "Borramos " + direccion + "\r\n"
                               self.register2file()

            elif not Metodo in Lista:
                Destinatario = Linea[1]
                self.Send()
                if Booleano == True:
                    continue

    def Send(self):
        """
        Buscamos el destinatario en nuestro diccionario
        de direcciones para poder enviarle las respuestas
        """
        global Booleano, Destinatario, line
        line_list = line.split(" ")
        Cliente = " "
        for clave in dicc:
            if clave == Destinatario:
                Cliente = Destinatario
                IP = dicc[clave][0]
                PUERTO = dicc[clave][1]
                #Creamos el socket
                my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                my_socket.connect((IP, int(PUERTO)))
                my_socket.send(line + "\r\n")
                linea = my_socket.recv(1024)
                #una vez que nos hemos atado
                #analizamos el metodo del que se trata
                if line_list[0] == "INVITE":
                    fich.write(str(time.time()) + " Recibido " + line + "\r\n")
                    rcv_invite = linea.split("\r\n\r\n")[0:-1]
                    rcv_invite1 = rcv_invite[0:3]
                    rcv_invite2 = str(rcv_invite1)
                    fich.write(str(time.time()) + " Enviando respuesta de "\
                    + Destinatario + ": " + rcv_invite2 + "\r\n")
                    self.wfile.write(linea)
                elif line_list[0] == "ACK":
                    fich.write(str(time.time()) + " Recibido ACK sip: " \
                    + Destinatario + "\r\n")
                elif line_list[0] == "BYE":
                    print "Enviando " + linea
                    fich.write(str(time.time()) + " Recibido BYE sip: " + \
                    Destinatario + "\r\n")
                    self.wfile.write(linea)
                elif not line_list[0] in Lista:
                    print linea
                    fich.write(str(time.time()) + " " + linea + "\r\n")
                    self.wfile.write(linea)

        if Cliente != Destinatario:
            #Si el destinatario no se encuentra
            #en nuestro diccionario como cliente
            #se envia un mensaje de error al no encontrarlo
            self.wfile.write("SIP/2.0 404 User Not Found")
            booleano = True

if __name__ == "__main__":

    Lista = ["REGISTER", "INVITE", "BYE"]
    try:
        Config = sys.argv[1]
    except IndexError:
        sys.exit("Usage: python proxy_registrar.py config")

    dicc = {}
    Destinatario = []
    booleano = False
    line = []

    fichero = open(Config, "r")
    #Abrimos el fichero xml y leemos los datos
    lines = fichero.readlines()
    fichero.close()
    #Extraemos los datos del fichero xml
    #SErvidor
    line_server = lines[1].split(">")
    servidor = line_server[0].split("=")[1]
    Server = servidor.split(" ")[0][1:-1]
    #Puerto del proxy
    puerto = line_server[0].split("=")[3]
    PUERTO_PROX = puerto.split(" ")[0][1:-1]
    #Base de datos
    line_database = lines[2].split(">")
    database = line_database[0].split("=")[1]
    PATH_DATABASE = database.split(" ")[0][1:-1]
    #log del proxy
    line_log = lines[3].split(">")
    log = line_log[0].split("=")[1]
    PATH_LOGPROX = log.split(" ")[0][1:-1]

    fich = open(PATH_LOGPROX, "a")

    # Creamos servidor de eco y escuchamos

    print "Server: " + Server + " listening at port " + \
    PUERTO_PROX + "..." + "\r\n"
    print "Listening..."
    proxy_serv = SocketServer.UDPServer(("127.0.0.1", int(PUERTO_PROX)), Proxy)
    proxy_serv.serve_forever()
