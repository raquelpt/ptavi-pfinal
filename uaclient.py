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


try:
    CONFIG = sys.argv[1]
    METHOD = sys.argv[2].upper()
    OPTION = sys.argv[3]
    PRUEBA = []

    fich = open(CONFIG, 'r')
    line = fich.readlines()
    fich.close()

    #CLIENTE
    lineusuario = line[1].split(">")
    cuenta = lineusuario[0].split("=")[1]
    USUARIO = cuenta.split(" ")[0][1:-2]
    #SERVER
    lineserver = line[2].split(">")
    uaserver = lineserver[0].split("=")[1]
    SERVER = uaserver.split(" ")[0][1:-1]
    #Port
    puertserver = lineserver[0].split("=")[2]
    PORT = puertserver.split(" ")[0][1:-2]
    #Port AUDIO RTP
    lineaudiortp = line[3].split(">")
    rtpaudio = lineaudiortp[0].split("=")[1]
    PUERTO_AUDIO = rtpaudio.split(" ")[0][1:-2]
    #IP DEL PROXY
    lineipproxy = line[4].split(">")
    ipproxy = lineipproxy[0].split("=")[1]
    IP_PROXY = ipproxy.split(" ")[0][1:-1]
    #PUERTO DEL PROXY
    puertoproxy = lineipproxy[0].split("=")[2]
    PORT_PROXY = puertoproxy.split(" ")[0][1:-2]
    #LOG
    linelog = line[5].split(">")
    log = linelog[0].split("=")[1]
    PATH_LOG = log.split(" ")[0][1:-2]
    #PATH DEL AUDIO
    linedeaudio = line[6].split(">")
    pathaudio = linedeaudio[0].split("=")[1]
    PATH_AUDIO = pathaudio.split(" ")[0][1:-2]
    
    # Creamos el socket, lo configuramos y lo atamos a un servidor/puerto
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    my_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    my_socket.connect((IP_PROXY, int(PORT_PROXY)))

    fich = open(PATH_LOG, 'a')

    def pdata(my_socket):
        global PRUEBA
        my_socket.send(LINE)
        try:
            PRUEBA = my_socket.recv(1024)
        except socket.error:
            fich.write(str(time.time()) + " Error:No server listening at " + IP_PROXY + " port " + PORT_PROXY)
            sys.exit(str(time.time()) + " Error:No server listening at " + \
            IP_PROXY + " port " + PORT_PROXY )

    # Comprobamos si es correcto el numero de argumentos pasados

    if len(sys.argv) != 4:
        LINE = "Numero de argumentos incorrectos"
        print LINE
        raise SystemExit


except IndexError:
    LINE = "Usage: python uaclient.py config method option 1"
    print LINE
    raise SystemExit


method_list = ['REGISTER', 'INVITE', 'BYE']


if METHOD not in method_list:
    print "Usage: python uaclient.py config method option"
    raise SystemExit


if METHOD == "REGISTER":
    fich = open(PATH_LOG, 'a')
    Register = ": REGISTER sip:" + USUARIO + ":" + PORT + \
    " SIP/2.0 Expires: " + OPTION + '\r\n'
    fich.write(str(time.time()) + " Sent to " + IP_PROXY + \
    ":" + PORT_PROXY + Register)
    LINE = 'REGISTER ' + "sip:" + USUARIO
    LINE += ":" + PORT + " SIP/2.0 \r\n" + "Expires: " + OPTION + "\r\n"
    print LINE
    pdata(my_socket)
    reciv_register = PRUEBA.split('\r\n\r\n')[0:-1]
    if reciv_register == ['SIP/2.0 200 OK']:
        print "Recibido --", PRUEBA
        fich.write(str(time.time()) + " Received from " + IP_PROXY + \
        ":" + PORT_PROXY + ": 200 OK" + '\r\n')

    if OPTION == '0':
        fich.write(str(time.time()) + " Finishing...")
        fich.close()
        print "Terminando socket..."
        my_socket.close()
    else:
        fich.write(str(time.time()) + " Starting..." + '\r\n')

if METHOD == 'INVITE':
    fich = open(PATH_LOG, 'a')
    LINE = 'INVITE ' + "sip: " + OPTION + " SIP/2.0 \r\n"
    LINE += "Content-Type: application/sdp \r\n\r\n" + "v=0 \r\n"
    LINE += "o=" + USUARIO + " " + IP + ' \r\n'
    LINE += "s=vampireando"
    LINE += ' \r\n' + "t=0" + ' \r\n' + "m=audio " + PUERTO_AUDIO + \
    ' RTP' + '\r\n'
    fich.write(str(time.time()) + " Sent to " + IP_PROXY + ":" + \
    PORT_PROXY + ': ' + LINE + '\r\n')
    print LINE
    pdata(my_socket)

    try:
        if PRUEBA != "SIP/2.0 404 User Not Found":
            Puerto_RTP = PRUEBA.split(' ')[14]
            invite = PRUEBA.split('\r\n\r\n')[0:-1]
            reciv_inv = invite[0:3]
            invite1 = str(reciv_inv)
            print 'Recibido PROXY: ' + rcv_invite2
            fich.write(str(time.time()) + " Received from " + IP_PROXY + \
            ":" + PORT_PROXY + ': ' + invite1 + '\r\n')
            METHOD = "ACK"
            LINEA = METHOD + ' sip:' + OPTION + ' SIP/2.0\r\n'
            print '\r\n\r\n' + "Enviando: " + LINEA
            fich.write(str(time.time()) + " Sent to " + IP_PROXY + ":" + \
            PORT_PROXY + ': ' + LINEA)
            my_socket.send(LINEA)
            fich.write(str(time.time()) + ' Conexion audio RTP ' + '\r\n')
            aAejecutar = './mp32rtp -i ' + IP + ' -p ' + str(PORT) + \
            ' < ' + PATH_AUDIO
            print "Ejecutamos", aAejecutar
            os.system(aAejecutar)
            print ("Se ha ejecutado" + '\r\n\r\n')
        else:
            print PRUEBA
    except IndexError:
        fich.write(str(time.time()) + \
        " Error: El servidor no esta escuchando")
        sys.exit(str(time.time()) + \
        "  Error: El servidor no esta escuchando")

if METHOD == 'BYE':
    fich = open(PATH_LOG, 'a')
    BYE = 'BYE ' + "sip:" + OPTION + " SIP/2.0" + '\r\n'
    print BYE
    LINE = BYE
    fich.write(str(time.time()) + " Sent to " + IP_PROXY + \
    ":" + PORT_PROXY + ': ' + BYE + '\r\n')
    pdata(my_socket)
    reciv_bye = PRUEBA.split('\r\n\r\n')[0:-1]
    if reciv_bye == ['SIP/2.0 200 OK']:
        fich.write(str(time.time()) + " Received from " + IP_PROXY + \
        ":" + PORT_PROXY + ": 200 OK" + '\r\n')
        fich.close()
        print PRUEBA
        # Cerramos todo
        my_socket.close()
        print "Fin."
