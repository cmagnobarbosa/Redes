# coding= utf-8
"""
Este modulo vai simular a comunicação com servidor..
Modulo simula a iteração do servidor
"""
import socket
HOST = ''              # Endereco IP do Servidor
PORT = 5001            # Porta que o Servidor esta
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
        con.send('4O,3C,AP')
        msg = ""
    else:
        print msg

    while(True):
        msg = con.recv(1024)
        if len(msg)>0:
            print msg
        if msg == "Fim":
            print 'Finalizando conexao do cliente', cliente
            con.close()
