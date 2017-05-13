# coding= utf-8
import socket
import os
"""
Cliente
Tp de Redes - Truco
UFSJ
Carlos Magno
Lucas Geraldo

Requisitos:
*python 2.7
*pygame

Modulo de conexão.
Versão Inicial
"""


class Conexao:
    """Modulo de conexão com servidor"""

    def __init__(self):
        self.servidor_end = '127.0.0.1'     # Endereco IP do Servidor
        self.porta = self.ler_config()
        self.socket = ""                           # Porta que o Servidor esta
        # self.socket_conexao = None                #Socket de conexao.

    def ler_config(self):
        """Ler a configuração de porta do arquivo"""
        arquivo = open("config", "r")
        for i in arquivo:
            return int(i)

    def envia_mensagem(self, mensagem):
        """Envia mensagem para o servidor"""
        print mensagem
        self.socket.send(mensagem)

    def ler_socket(self):
        """Realiza a leitura do socket e retorna os dados que foram lidos."""
        retorno = None
        retorno = self.socket.recv(32)
        if retorno is not None and len(retorno) > 0:
            # print"Retorno ", retorno

            return retorno

    def encerra_conexao(self):
        "Encerra a conexao com servidor."
        print "Encerrando a conexão"
        self.socket.close()
        exit()

    def conectar(self):
        """Conecta e salva o socket de conexao"""
        try:
            socket_conexao = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            destino = (self.servidor_end, self.porta)
            servidor = socket_conexao.connect(destino)

        except Exception as e:
            print " Erro de conexão.. verifique se o servidor está ativo."
            print "Endereço informado ", self.servidor_end, " ", self.porta
            exit()
        self.socket = socket_conexao
