# coding= utf-8
import socket
import os
HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 5000            # Porta que o Servidor esta
"""
socket.AF_INET
These constants represent the address (and protocol) families,
used for the first argument to socket(). If the AF_UNIX constant is not
defined then this protocol is unsupported.

socket.SOCK_STREAM
These constants represent the socket types,
used for the second argument to socket().
(Only SOCK_STREAM and SOCK_DGRAM appear to be generally useful.)
"""
try:
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
except Exception as e:
    print " Erro de conexão.. verifique se o servidor está ativo."
    exit()


print 'Para sair use CTRL+X\n'
msg = raw_input("Digite uma mensagem:\n")
while msg <> '\x18':
    tcp.send(msg)
    msg = raw_input()
tcp.close()
