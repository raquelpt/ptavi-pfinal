#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
Clase (y programa principal) para un servidor en SIP
"""


import SocketServer
import sys
import os
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


Direccion = ""
P_Servi = ""
P_rtp = ""


class ServidorHandler(ContentHandler):

    def __init__(self):

        """
        Inicializando el diccionario
        """

        self.diccionario = {}


    def startElement(self, name, attrs):

        """
        Añadiendo atributos al diccionario
        """

        if name == "account":
            username = attrs.get("username", "")
            self.diccionario["userName"] = username
        if name == "uaserver":
            ip = attrs.get("ip", "127.0.0.1")
            puerto = attrs.get("puerto", "")
            self.diccionario["servIp"] = ip
            self.diccionario["servPort"] = puerto
        if name == "rtpaudio":
            puerto = attrs.get("puerto", "")
            self.diccionario["rtpPort"] = puerto
        if name == "regproxy":
            ip = attrs.get("ip", "")
            puerto = attrs.get("puerto", "")
            self.diccionario["proxIp"] = ip
            self.diccionario["proxPort"] = puerto
        if name == "log":
            path = attrs.get("path", "")
            self.diccionario["logPath"] = path
        if name == "audio":
            path = attrs.get("path", "")
            self.diccionario["audioPath"] = path


    def get_attrs(self):

        """
        Lista con los atributos
        """

        return self.diccionario


class SipHandler(SocketServer.DatagramRequestHandler):
    
    def handle(self):
        while 1:

            # Leyendo línea a línea lo que nos envía el cliente

            line = self.rfile.read()

            # Si no hay más líneas salimos del bucle infinito
            if not line:

                break
            # Seleccionamos la respuesta correcta

            print "El cliente nos manda " + line

            Metodo = line.split(" ")[0]

            if Metodo == "INVITE" or Metodo == "ACK" or Metodo == "BYE":

                if Metodo == "INVITE" and \

                    line.split(" ")[2] == 'SIP/2.0\r\n\r\n':



                    Answer = "SIP/2.0 100 Trying\r\n\r\n"

                    Answer += "SIP/2.0 180 Ringing\r\n\r\n"

                    Answer += "SIP/2.0 200 OK\r\n\r\n"

                    Answer += "ContentType: application/sdp" + "\r\n\r\n"

                    Answer += "v=0" + "\r\n"

                    Answer += "o=" + Direccion + " " + P_Server + "\r\n"

                    Answer += "s=misesion" + "\r\n"

                    Answer += "t=0" + "\r\n"

                    Answer += "m=audio " + P_rtp + " RTP" + "\r\n\r\n"

                    self.wfile.write(Answer)

                    print(Answer)

                    accion = "Enviar a " + str(ProxIp) + ":"

                    accion += str(ProxPort)

                    log(accion, Answer, fich_log)



                elif Metodo == "ACK":

                    # Tratamiento ACK

                    aEjecutar = "mp32rtp -i 127.0.0.1 -p" + P_rtp + \ 
                    " < " + FICHERO_AUDIO

                    print "Vamos a ejecutar", aEjecutar

                    os.system(aEjecutar)

                    accion = "Recivido de " + str(ProxyIp) + ":"

                    accion += str(Proxy_Port)

                    Answer = FICHERO_AUDIO

                    log(accion, Answer, fich_log)

                elif Metodo == "BYE":

                    # Tratamiento BYE

                    Answer = "SIP/2.0 200 OK\r\n\r\n"

                    self.wfile.write(Answer)

                    accion = "Sent to " + str(ProxIp) + ":"

                    accion += str(ProxPort) + ":"

                    log(accion, Answer, fich_log)

                else:

                    Answer = "SIP/2.0 400 Bad Request"

                    accion = "Sent to " + str(ProxIp) + ":"

                    accion += str(ProxPort) + ":"

                    log(accion, Answer, fich_log)

            else:

                Answer = "SIP/2.0 405 Method Not Allowed"

                accion = "Sent to " + str(ProxIp) + ":"

                accion += str(ProxPort) + ":"

                log(accion, Answer, fich_log)



            # Imprimimos la respuesta y la enviamos



            if Metodo != "ACK":

                print "Enviamos:" + Answer

                self.wfile.write(Answer)



    def log(self, accion, linea, logFile):

        """

        Metodo para poder imprimir debug por pantalla y log en el fichero

        """



        tiempo = time.strftime('%Y%m%d%H%M%S', time.gmtime(time.time()))

        line = linea.split("\r\n", " ")

        texto = ' '.join(line)

        logFile = open(LOG_FILE, 'a')

        logFile.write(tiempo + ' ' + line + '\n')

        logFile.close()



if __name__ == "__main__":



    if len(sys.argv) != 2:

        print "Usage: python uaserver.py config"

        raise SystemExit



    Config = sys.argv[1]



    parser = make_parser()

    Datos = SipHandler()

    parser.setContentHandler(Datos)

    parser.parse(open(Config))



    Dicc = SipHandler_Datos.get_attrs()

    USERNAME = Dicc['userName']

    IP = Dicc['servIp']

    PORT = int(Dicc['servPort'])

    RTP_PORT = Dicc['rtpPort']

    PROXY_IP = Dicc['proxIp']

    PROXY_PORT = Dicc['proxPort']

    LOG = Dicc['logPath']

    AUDIO = Dicc['audioPath']



    Direccion = USERNAME + '@dominio.com'

    log('', '', '', 'Starting...')



    try:



        serv = SocketServer.UDPServer((IP, PORT), SipHandler)

        print "Listening..."

        serv.serve_forever()
