# coding= utf-8
import socket
import os
"""
Modulo de conexão.
Versão Inicial
"""


class Conexao:
    """Modulo de conexão com servidor"""

    def __init__(self):
        self.servidor_end = '127.0.0.1'     # Endereco IP do Servidor
        self.porta = 5001                   # Porta que o Servidor esta

    def conectar(self):
        try:
            socket_conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            destino = (self.servidor_end, self.porta)
            servidor = socket_conexao.connect(destino)

        except Exception as e:
            print " Erro de conexão.. verifique se o servidor está ativo."
            print "Endereço informado ", self.servidor_end, " ", self.porta
            exit()

        mensagem = "Quero Jogar"
        socket_conexao.send(mensagem)
        resposta = socket_conexao.recv(1024)
        if resposta is not None:
            print"Resposta do Servidor:", resposta
        socket_conexao.close()
