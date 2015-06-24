#Practica final PTAVI
#!/usr/bin/python
# -*- coding: iso-8859-15 -*-

"""
Programa cliente que abre un socket a un servidor
"""


import socket
import sys
import os
import time
from xml.sax import make_parser
from xml.sax.handler import ContentHandler


method_list = ['REGISTER', 'INVITE', 'BYE']

# Comprobamos si es correcto el numero de argumentos pasados
if len(sys.argv) != 4:
    print "Usage: python uaclient.py config method option"
    raise SystemExit

# Cliente UDP simple.
try:
	CONFIG = sys.argv[1]
	METHOD = sys.argv[2].upper()
	if METHOD not in method_list:
		print "Usage: python uaclient.py config method option"
		raise SystemExit

	OPTION = sys.argv[3]
	
	fich = open(CONFIG, 'r')
        line = fich.readlines()
	fich.close()

    #Extraemos el contenido del fichero
    
    #CLIENTE
    lineusuario = line[1].split(">")
    cuenta = lineusuario[0].split("=")[1]
    USUARIO = cuenta.split(" ")[0][1:-1]
    #SERVER
    lineserver = line[2].split(">")
    uaserver = lineserver[0].split("=")[1]
    SERVER = uaserver.split(" ")[0][1:-1]
    #Port
    puertserver = lineserver[0].split("=")[2]
    PORT = puertserver.split(" ")[0][1:-1]
    #Port AUDIO RTP
    lineaudiortp = line[3].split(">")
    rtpaudio = lineaudiortp[0].split("=")[1]
    PUERTO_AUDIO = rtpaudio.split(" ")[0][1:-1]
    #IP DEL PROXY
    lineipproxy = line[4].split(">")
    ipproxy = lineipproxy[0].split("=")[1]
    IP_PROXY = ipproxy.split(" ")[0][1:-1]
    #PUERTO DEL PROXY
    puertoproxy = lineipproxy[0].split("=")[2]
    PORT_PROXY = puertoproxy.split(" ")[0][1:-1]
    #LOG
    linelog = line[5].split(">")
    log = linelog[0].split("=")[1]
    PATH_LOG = log.split(" ")[0][1:-1]
    #PATH DEL AUDIO
    linedeaudio = line[6].split(">")
    pathaudio = linedeaudio[0].split("=")[1]
    PATH_AUDIO = pathaudio.split(" ")[0][1:-1]

    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP_PROXY, int(PUERTO_PROXY)))

    fich = open(PATH_LOG, 'r+')
    
   

# Contenido que vamos a enviar



LINE = METODO + " sip:" + Direccion.split(":")[0] + " SIP/2.0\r\n\r\n"











print "Enviando: " + LINE

my_socket.send(LINE)

try:

    data = my_socket.recv(1024)

except socket.error:

    print ('Error:No server listening at ' + str(SERVER) + ' port ' + int(PORT))

    raise SystemExit



print 'Recibido --', data

line = data.split('\r\n\r\n')[:-1]



if line == ["SIP/2.0 100 Trying", "SIP/2.0 180 Ringing", "SIP/2.0 200 OK"]:

    LINE = "ACK sip:" + Direccion.split(":")[0] + " SIP/2.0\r\n\r\n"

    my_socket.send(LINE)

elif line == ["SIP/2.0 400 Bad Request"]:

    print "El servidor no entiende la petición"



elif line == ["SIP/2.0 405 Method Not Allowed"]:

    print "Enviado metodo incorrecto"
    
print "Terminando socket..."
# Cerramos todo
my_socket.close()
print "Fin."
