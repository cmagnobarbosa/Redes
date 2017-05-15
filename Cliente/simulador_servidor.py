# coding= utf-8
"""
Este modulo vai simular a comunicação com servidor..
Modulo simula a iteração do servidor

Padrão da mensagem
"0 0 1 2 000000 0201 ab0 03 0 0 0 2e4p5o6c 0"
sem os espaços...
"""
import socket
import time


def ler_config():
    arquivo = open("config", "r")
    for i in arquivo:
        return int(i)

HOST = ''              # Endereco IP do Servidor
PORT = ler_config()    # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(2)
lista = []
print "Aguardando cliente..."
while(True):
    con, cliente = tcp.accept()
    if con in lista:
        break
    print con
    lista.append(con)
    print 'Conectado por', cliente
    """
    1024 size the read.
    """

    msg = con.recv(1024)
    print "enviado"
    con.send('1a104p7c7o000000000000000000000')
    msg = ""

    while(True):
        msg = con.recv(1024)
        if len(msg) > 0:
            print msg
            time.sleep(5)
            #0012 000000 0201 ab0 03 0 0 0 2e4p5o6c 0"
            con.send("00020000000201ab0030002e4p5o6c0")
            time.sleep(5)
            con.send("00120000000201ab0030002e4p5o6c0")
        if msg == "Fim":
            """Encerra a conexao e fecha o cliente"""
            print "Fim de Jogo", 'Finalizando conexao do cliente', cliente
            con.close()
            exit()
