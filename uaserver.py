#!/usr/bin/python
# -*- coding: iso-8859-15 -*-
"""
Clase (y programa principal) para un servidor en SIP
"""

import SocketServer
import sys
import os
import os.path
import socket




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
			# Comprobamos el metodo que nos han mandado
            if Metodo == "INVITE" or Metodo == "ACK" or Metodo == "BYE":
				
                if Metodo == "INVITE":
					# Si el metodo es invite enviamos la correspondiente 
					# respuesta
                    Answer = 'SIP/2.0 100 Trying' + '\r\n\r\n'
                    Answer += "SIP/2.0 180 Ringing\r\n\r\n"
                    Answer += "SIP/2.0 200 OK\r\n\r\n"
                    Answer += "ContentType: application/sdp" + "\r\n\r\n"
                    Answer += "v=0" + "\r\n"
                    Answer += "o=" + USUARIO + " " + IP + "\r\n"
                    Answer += "s=misesion" + "\r\n"
                    Answer += "t=0" + "\r\n"
                    Answer += "m=audio " + str(PUERTO_AUDIO) + " RTP" + "\r\n\r\n"
                    self.wfile.write(Answer)
                    print(Answer)

                elif Metodo == "ACK":
                    # Tratamiento ACK
                    aEjecutar = "mp32rtp -i 127.0.0.1 -p" + str(PUERTO_AUDIO) + " < " + PATH_AUDIO
                    print "Vamos a ejecutar", aEjecutar
                    os.system(aEjecutar)
                elif Metodo == "BYE":
                    # Tratamiento BYE
                    Answer = "SIP/2.0 200 OK\r\n\r\n"
                    self.wfile.write(Answer)
                    print (Answer)
            else:
				# No se trata de ninguno de los metodos permitidos
                Answer = "SIP/2.0 405 Method Not Allowed"
                print Answer
                self.wfile.write(Answer)



if __name__ == "__main__":


	if len(sys.argv) != 2:
	    print "Usage: python uaserver.py config"
	    raise SystemExit

    Config = sys.argv[1]

	print "Listening..."

    fich = open(Config, 'r')
    line = fich.readlines()
    fich.close()


    #CLIENTE
    lineusuario = line[1].split(">")
    cuenta = lineusuario[0].split("=")[1]
    USUARIO = cuenta.split(" ")[0][1:-1]
    #IP
    lineserver = line[2].split(">")
    uaserver = lineserver[0].split("=")[1]
    IP = uaserver.split(" ")[0][1:-1]
    #Port
    puertserver = lineserver[0].split("=")[2]
    PORT = puertserver.split(" ")[0][1:-1]
    #IP DEL PROXY
    lineipproxy = line[4].split(">")
    ipproxy = lineipproxy[0].split("=")[1]
    IP_PROXY = ipproxy.split(" ")[0][1:-1]
    #PUERTO DEL PROXY
    puertoproxy = lineipproxy[0].split("=")[2]
    PORT_PROXY = puertoproxy.split(" ")[0][1:-1]
	#Port AUDIO RTP
    lineaudiortp = line[3].split(">")
    rtpaudio = lineaudiortp[0].split("=")[1]
    PUERTO_AUDIO = rtpaudio.split(" ")[0][1:-1]
    #PATH DEL AUDIO
    linedeaudio = line[6].split(">")
    pathaudio = linedeaudio[0].split("=")[1]
    PATH_AUDIO = pathaudio.split(" ")[0][1:-1]

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP_PROXY, int(PORT_PROXY)))
	
    serv = SocketServer.UDPServer(("127.0.0.1", int(PORT)), SipHandler)
    serv.serve_forever()
