# coding: utf-8

if __name__ != '__main__':

    baralho = {
        "ap": " A paus",
        "ac": " A copas",
        "ae": " A espada",
        "ao": " A ouro",
        "2p": " 2 paus",
        "2c": " 2 copas",
        "2e": " 2 espada",
        "2o": " 2 ouro",
        "3p": " 3 paus",
        "3c": " 3 copas",
        "3e": " 3 espada",
        "3o": " 3 ouro",
        "4p": " 4 paus",
        "4c": " 4 copas",
        "4e": " 4 espada",
        "4o": " 4 ouro",
        "5p": " 5 paus",
        "5c": " 5 copas",
        "5e": " 5 espada",
        "5o": " 5 ouro",
        "6p": " 6 paus",
        "6c": " 6 copas",
        "6e": " 6 espada",
        "6o": " 6 ouro",
        "7p": " 7 paus",
        "7c": " 7 copas",
        "7e": " 7 espada",
        "7o": " 7 ouro",
        "qp": " q paus",
        "qc": " q copas",
        "qe": " q espada",
        "qo": " q ouro",
        "jp": " J paus",
        "jc": " J copas",
        "je": " J espada",
        "jo": " J ouro",
        "kp": " K paus",
        "kc": " K copas",
        "ke": " K espada",
        "ko": " K ouro",
        "00": " "
    }


def info(mensagem):
    """
    Informa ao cliente a situação do jogo, sempre que algum outro jogador
    realiza alguma ação
    """

    print "******************************* Info *****************************"

    print ("Mesa\nid 0: %s | id 1: %s | id 2: %s | id 3: %s"
           % (traduz(mensagem[22:24]), traduz(mensagem[24:26]),
              traduz(mensagem[26:28]), traduz(mensagem[28:30])))

    print ("\nPlacar da Rodada:[%s] [%s] [%s]"
           % (mensagem[14:15], mensagem[15:16], mensagem[16:17]))

    print ("\nValor da Rodada: " + mensagem[17:19])

    print ("\nPlacar do jogo\nA: %s \t B: %s"
           % (mensagem[10:12], mensagem[12:14]))

    print "******************************************************************\n"


def takeCards(cartas):
    """
    Retorna a lista de strngs 'mao' com as cartas recebidas
    pelo jogador apos uma nova distribuição
    """

    mao = []
    mao.append(cartas[0:2])
    mao.append(cartas[2:4])
    mao.append(cartas[4:6])
    return mao


def acao(mensagem, cliente_Id, cliente_Eq, cliente_mao):
    print "\nSua vez:"
    opcoes = []
    cont = 0
    op = ''
    l = ['1', '2']
    valor = int(mensagem[17:19])
    placarA = mensagem[10:12]
    placarB = mensagem[12:14]

    # Caso o adversario tenha pedido truco
    if(mensagem[19:20] == "1"):
        if(mensagem[17:19] == "01"):
            print "\n\t Seu adversario pediu truco..."
        else:
            print "\n\t Seu adversario pediu", valor + 3

        print "Escolha:"
        while(op not in l):
            print "1 - Aceitar"
            print "2 - Correr"
            op = raw_input("Opçao: ")
            if(op not in l):
                print "\nOpção inválida!\nEscolha:"

        mensagem = respTruco(mensagem, op)
        return mensagem

    # Caso haja a possibilidade de pedir truco
    elif(valor < 12 and
            (mensagem[20:21] == "0" or mensagem[20:21] == cliente_Eq) and
         (placarA is not "11" and placarB is not "11")):

        # Caso o usuario digite uma opção invalida
        while(op not in l):
            print "1 - Jogar Carta"
            if(mensagem[17:19] == "01"):
                print "2 - Pedir truco"
            else:
                print "2 - Pedir %d" % (int(mensagem[17:19]) + 3)
            op = raw_input("Opçao: ")
            if(op not in l):
                print "\nOpção inválida!\nSua vez:"
    else:
        op = "1"

    # Jogar carta
    if(op is "1"):
        while(op not in opcoes):
            print "\nEscolha uma carta para jogar:"
            opcoes = []
            cont = 0
            for i in cliente_mao:
                print cont, "-", traduz(i)
                opcoes.append(cont)
                cont += 1

            op = raw_input("Opçao: ")
            try:
                op = int(op)
                if(op not in opcoes):
                    print "\nOpção invalida! Digite uma das opções disponiveis"
            except Exception:
                print "\nOpção invalida! Digite uma das opções disponiveis"

        mensagem = jogarCarta(mensagem, cliente_mao, op, cliente_Id)
        return mensagem

    # Pedir truco
    elif(op is "2"):
        mensagem = pedirTruco(mensagem)
        return mensagem


def jogarCarta(mensagem, cliente_mao, op, cliente_Id):
    """
    Realiza alteração na mensagem,
    inserindo no campo 'mesa' a carta jogada pelo cliente
    """
    mensagem_aux = ''

    if(cliente_Id == '0'):
        mensagem_aux += mensagem[:22]
        mensagem_aux += cliente_mao[op]
        mensagem_aux += mensagem[24:]
        cliente_mao.pop(op)

    if(cliente_Id == '1'):
        mensagem_aux += mensagem[:24]
        mensagem_aux += cliente_mao[op]
        mensagem_aux += mensagem[26:]
        cliente_mao.pop(op)

    if(cliente_Id == '2'):
        mensagem_aux += mensagem[:26]
        mensagem_aux += cliente_mao[op]
        mensagem_aux += mensagem[28:]
        cliente_mao.pop(op)

    if(cliente_Id == '3'):
        mensagem_aux += mensagem[:28]
        mensagem_aux += cliente_mao[op]
        mensagem_aux += mensagem[30:]
        cliente_mao.pop(op)

    return mensagem_aux


def traduz(cartas):
    """
    Traduz a sigla referente a cada carta, para seu nome completo
    """

    aux = ''

    if(len(cartas) > 2):
        aux += baralho[cartas[0:2]]
        aux += baralho[cartas[2:4]]
        aux += baralho[cartas[4:6]]

    else:
        aux = baralho[cartas]

    return aux


def pedirTruco(mensagem):
    mensagem_aux = ''

    mensagem_aux += mensagem[:19]
    mensagem_aux += "1"
    mensagem_aux += mensagem[20:]

    print "\n\tAguardando resposta do oponente..."

    return mensagem_aux


def respTruco(mensagem, op):
    mensagem_aux = ''

    mensagem_aux += mensagem[:21]
    if(op == "1"):
        mensagem_aux += "1"  # Aceitar truco
    elif(op == "2"):
        mensagem_aux += "0"  # Correr do truco
    mensagem_aux += mensagem[22:]

    return mensagem_aux
