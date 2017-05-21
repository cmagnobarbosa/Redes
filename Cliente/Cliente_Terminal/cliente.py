# coding: utf-8
import socket
from truco import *


def main():
    # Dados do cliente para conexao como server
    ipServidor = ''
    portaServidor = 5000

    # Variaveis
    cliente_mao = []
    cliente_Id = ''
    cliente_Eq = ''
    mensagem = ''

    # Cria o objeto socket e conecta ao servidor
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Definicao do servidor como TCP IP

    try:
        # Estabelecendo conexão com o servidor
        cliente.connect((ipServidor, portaServidor))
        print "Cliete conectado ao servidor!"

    except Exception:
        print "Erro ao conectar ao servidor!"
        return None

    print "\n--------------- Inicio do jogo ----------------\n"
    mensagem = cliente.recv(31)
    cliente_Id = mensagem[:1]
    cliente_Eq = mensagem[1:2]
    cliente_mao = takeCards(mensagem[4:10])

    if(cliente_Id is "0"):
        print "Seu Id é 0\nsua equipe é 'a' -> Ids(0 e 2)\n"
    elif(cliente_Id is "1"):
        print "Seu Id é 1\nsua equipe é 'b' -> Ids(1 e 3)"
    elif(cliente_Id is "2"):
        print "Seu Id é 2\nsua equipe é 'a' -> Ids(0 e 2)"
    elif(cliente_Id is "3"):
        print "Seu Id é 3\nsua equipe é 'b' -> Ids(1 e 3)"
    print "Nova rodada! Sua mão é:", traduz(mensagem[4:10])

    while True:
        mensagem = cliente.recv(31)
        placarA = int(mensagem[10:12])
        placarB = int(mensagem[12:14])

        # Se o jogo ja tiver um vencedor
        if(placarA >= 12 or placarB >= 12):
            break

        # O servidor enviou uma nova mao para o cliente
        if(mensagem[4:5] is not "0"):
            cliente_mao = takeCards(mensagem[4:10])
            print "\nNova rodada! Sua mão é:", traduz(mensagem[4:10]), "\n"
            info(mensagem)

        else:
            if(mensagem[2:3] is "1"):  # Vez do cliente
                mensagem = acao(mensagem, cliente_Id, cliente_Eq, cliente_mao)
                cliente.send(mensagem)

            elif(mensagem[2:3] is "0" and mensagem[19:20] is not "1"):
                info(mensagem)

    if(int(mensagem[10:12]) >= 12):
        print "\n\tFim de jogo! Equipe A venceu o jogo!\n"

    if(int(mensagem[12:14]) >= 12):
        print "\n\tFim de jogo! Equipe B venceu o jogo!\n"

        cliente.close()

if __name__ == '__main__':
    main()
