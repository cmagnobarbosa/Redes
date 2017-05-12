# coding= utf-8
"""
Este modulo vai simular a comunicação com servidor..
Modulo simula a iteração do servidor
"""
import socket
import time
HOST = ''              # Endereco IP do Servidor
PORT = 5002            # Porta que o Servidor esta
tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
orig = (HOST, PORT)
tcp.bind(orig)
tcp.listen(2)
lista=[]
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
    if msg == "0,0,0,0":
        "Inicio do jogo"
        print "The begin"
        con.send('2p,7c,ap')
        msg = ""
    else:
        print msg

    while(True):
        msg = con.recv(1024)
        if len(msg)>0:
            print msg
            time.sleep(1)
            con.send("1")
        if msg == "Fim":
            """Encerra a conexao e fecha o cliente"""
            print "Fim de Jogo",'Finalizando conexao do cliente', cliente
            con.close()
            exit()
