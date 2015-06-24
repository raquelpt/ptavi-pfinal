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
        

if __name__ == "__main__":


    if len(sys.argv) != 2:

        print "Usage: python uaserver.py config"
        raise SystemExit


    Config = sys.argv[1]

    USERNAME = Dicc['userName']
    IP = Dicc['servIp']
    PORT = int(Dicc['servPort'])
    RTP_PORT = Dicc['rtpPort']
    PROXY_IP = Dicc['proxIp']
    PROXY_PORT = Dicc['proxPort']
    LOG = Dicc['logPath']
    AUDIO = Dicc['audioPath']

    Direccion = USERNAME + '@dominio.com'


    try:

        serv = SocketServer.UDPServer((IP, PORT), SipHandler)
        print "Listening..."
        serv.serve_forever()
