# coding: utf-8

import pygame
import sys
from pygame.locals import *
from gui import *
from conexao import *
from jogador import *
from Queue import Queue
from threading import Thread

"""
Cliente
Tp de Redes - Truco
UFSJ
Carlos Magno
Lucas Geraldo

Requisitos:
*python 2.7
*pygame
Modulo Principal.

"""


class Principal(Gui):
    """
    Classe Principal
    """

    def __init__(self):
        #---HABILITAR BOTAO TRUCO---
        # Ative para ativar a opção de pedir truco..
        self.truco_habilitado = 1
        #--------------------

        self.mensagem_servidor = ""
        self.carta_selecionada = -1
        self.sua_vez = 0
        self.conexao = Conexao()
        self.conexao.conectar()
        self.gui = Gui()
        self.jogador = Jogador()
        self.recebe_cartas()
        self.gui.carrega_cartas()
        #--------------------
        self.pede_truco="0"
        self.rodada = 1
        self.gui.valor_rodada = "0"
        self.flag_truco = 0
        self.gui.pontos = "0000"
        self.gui.partidas = "000"
        self.question_truco = "0"
        self.proposta_truco_equipe = "0"
        self.resposta_proposta_truco = "0"
        self.mesa_jogo = "000000"
        self.gui.mensagem_vez = "Aguarde..."
        self.gui.cont_cartas = 3
        #-----------------
        self.quee = Queue()

        self.verifica = Thread(target=self.verifica_resposta_servidor, args=(
            self.quee, self.conexao))
        self.verifica.daemon = True
        self.verifica.start()

    def atualiza_mensagem(self):
        "Atualiza o campo de mensagens.."

        if(self.sua_vez is 0):

            self.gui.mensagem_vez = "Aguarde..."
            self.gui.escrever(self.gui.mensagem_vez, (40, 430), (255, 0, 0))
        if(self.sua_vez is 1):

            self.gui.mensagem_vez = "Sua Vez..."
            self.gui.escrever(self.gui.mensagem_vez, (40, 430), (0, 255, 0))

    def agrupa_cartas(self, lista):
        """Agrupa as cartas recebidas do servidor"""
        final = ""
        c1 = ""
        for i in lista:
            c1 = c1 + i
            if(len(c1) == 2):
                final = final + c1 + ","
                c1 = ""
        lista = final.split(',')
        lista.pop()

        return lista

    def recebe_cartas(self):
        """
        Carrega as cartas recebidas do servidor.
        Extrai os dados iniciais da primeira conexão.

        """

        # self.conexao.envia_mensagem("0")
        self.mensagem_servidor = self.conexao.ler_socket()
        # print "Me", self.mensagem_servidor
        #--Extrai os dados iniciais...
        self.jogador.id = self.mensagem_servidor[0:1]
        self.jogador.equipe = self.mensagem_servidor[1:2]
        self.sua_vez = int(self.mensagem_servidor[2:3])
        cartas = self.mensagem_servidor[4:10]
        print "ID ", self.jogador.id, "Equipe ", self.jogador.equipe, "Sua Vez ", self.sua_vez
        self.jogador.cartas_mao = cartas

        cartas = self.agrupa_cartas(cartas)
        for i in cartas:
            self.gui.cartas_recebidas.append(i)

    def verifica_resposta_servidor(self, fila, conexao):
        """Verifica a conexao.."""
        while (True):
            palavra = conexao.ler_socket()
            if(palavra is not None):
                self.quee.put(palavra)

    def processa_resposta(self, lista):
        """Vai processar a mensagem recebida"""
        self.mensagem_servidor = lista
        if(lista is not None):
            print "resposta vinda do servidor ", lista
            self.sua_vez = int(lista[2:3])
            self.atualiza_mensagem()
            self.finaliza_rodada(int(lista[3:4]))
            self.rodada = int(lista[3:4])
            cartas = lista[4:10]
            if(cartas != "000000"):
                # Considerando que nos decorrer das partida o servidor não envia as
                # cartas. Redefine a mão do jogador.
                self.gui.cartas_recebidas = []
                self.jogador.cartas_mao = cartas
                cartas = self.agrupa_cartas(cartas)
                for i in cartas:
                    self.gui.cartas_recebidas.append(i)
            self.gui.pontos = lista[10:14]
            self.gui.partidas = lista[14:17]
            self.gui.valor_rodada = lista[17:19]
            self.question_truco = lista[19:20]
            self.proposta_truco_equipe = lista[20:21]
            self.mesa_jogo = lista[22:30]
            self.renderiza_mesa()

            print self.sua_vez
            if(self.gui.cont_cartas > 1):
                self.gui.cont_cartas = self.gui.cont_cartas - 1

    def renderiza_mesa(self):
        """Função que renderiza_mesa"""
        # 00 00 00 00
        self.gui.caminho_cartas
        print self.mensagem_servidor
        cartas = self.agrupa_cartas(self.mesa_jogo)
        print "Cartas Mesa ", cartas
        cont = -1
        for i in cartas:
            cont = cont + 1
            # self.gui.renderiza_cartas_jogadas(i,self.gui.pos_cartas_jog_1)
            # self.gui.update_card_adversario(1,self.cont_cartas)
            if not i == "00":
                i = self.gui.caminho_cartas + i + ".png"

                if(self.jogador.id == "0"):
                    if cont is 0:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.sua_pos_carta)

                    if cont is 1:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_1)
                        self.gui.update_card_adversario(
                            1, self.gui.cont_cartas)
                    if cont is 2:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_2)
                        self.gui.update_card_adversario(
                            2, self.gui.cont_cartas)
                    if cont is 3:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_3)
                        self.gui.update_card_adversario(
                            3, self.gui.cont_cartas)

                elif(self.jogador.id == "1"):
                    if cont is 0:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_3)
                        self.gui.update_card_adversario(
                            3, self.gui.cont_cartas)
                    elif cont is 1:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.sua_pos_carta)

                    elif cont is 2:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_1)
                        self.gui.update_card_adversario(
                            1, self.gui.cont_cartas)

                    elif cont is 3:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_2)
                        self.gui.update_card_adversario(
                            3, self.gui.cont_cartas)

                elif(self.jogador.id == "2"):
                    if cont is 0:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_2)
                        self.gui.update_card_adversario(
                            2, self.gui.cont_cartas)
                    elif cont is 1:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_3)
                        self.gui.update_card_adversario(
                            3, self.gui.cont_cartas)
                    elif cont is 2:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.sua_pos_carta)

                    elif cont is 3:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_1)
                        self.gui.update_card_adversario(
                            1, self.gui.cont_cartas)

                elif (self.jogador.id == "3"):
                    if cont is 0:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_1)
                        self.gui.update_card_adversario(
                            1, self.gui.cont_cartas)
                    elif cont is 1:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_2)
                        self.gui.update_card_adversario(
                            2, self.gui.cont_cartas)

                    elif cont is 2:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.pos_cartas_jog_3)
                        self.gui.update_card_adversario(
                            3, self.gui.cont_cartas)

                    elif cont is 3:
                        self.gui.renderiza_cartas_jogadas(
                            i, self.gui.sua_pos_carta)

    def finaliza_rodada(self, valor):
        """Verifica se a rodada terminou e limpa a tela"""
        if(int(self.rodada) is not valor):
            self.gui.tela_padrao(self.jogador.equipe)
            print "Limpando a rodada"

    def prepara_mensagem(self, carta_jogada):
        """Prepara uma mensagem da carta jogada para o envio"""
        print "Mensagem ", self.mensagem_servidor
        # acerta o id
        self.mensagem_servidor = self.mensagem_servidor[
            :0] + "0" + self.mensagem_servidor[1:]

        # Acerta a equipe
        self.mensagem_servidor = self.mensagem_servidor[
            :1] + "0" + self.mensagem_servidor[2:]
        # Limpa mao..
        self.mensagem_servidor = self.mensagem_servidor[
            :4] + "000000" + self.mensagem_servidor[10:]

        # Acerta a posicao da carta na mesa
        if(int(self.jogador.id) is 0):
            self.mensagem_servidor = self.mensagem_servidor[
                :22] + carta_jogada + self.mensagem_servidor[24:]
        if(int(self.jogador.id) is 1):
            self.mensagem_servidor = self.mensagem_servidor[
                :24] + carta_jogada + self.mensagem_servidor[26:]
        if(int(self.jogador.id) is 2):
            self.mensagem_servidor = self.mensagem_servidor[
                :26] + carta_jogada + self.mensagem_servidor[28:]
        if(int(self.jogador.id) is 3):
            self.mensagem_servidor = self.mensagem_servidor[
                :28] + carta_jogada + self.mensagem_servidor[30:]

    def verifica_proposta_truco(self):
        """Exibe a tela de Truco"""
        if(self.question_truco == "1") and self.sua_vez is 1:
            self.gui.tela_truco()

    def solicita_truco(self):
        """Solicitar Truco"""

        if(self.sua_vez is 1):
            print "Solicitando Truco.."
            self.mensagem_servidor = self.mensagem_servidor[
                :19] + self.pede_truco + self.mensagem_servidor[20:]
            print "Mensagem enviada na solicitação de Truco..", self.mensagem_servidor
            self.pede_truco ="0"

    def responde_truco(self):
        """Envia uma mensagem para o servidor com a resposta do truco"""

        self.mensagem_servidor = self.mensagem_servidor[
            :21] + self.resposta_proposta_truco + self.mensagem_servidor[22:]

        print "Enviando a Seguinte resposta de Truco ", self.mensagem_servidor
        self.conexao.envia_mensagem(self.mensagem_servidor)

    def envia_carta_servidor(self, carta_jogada):
        """Dispara cartas para o servidor e altera os campos necessarios.."""
        if carta_jogada is not None:
            carta_jogada = carta_jogada.split("/")[1].split(".")[0]
            # 1(ID)|a(Equipe)|0(vez)|0(rodada)|4p7c7o(mao)|0000(placar_jogo)|000(placar_rodada)|00(valor
            # rodada)|0(question)|0(equipe question)|0(resposta
            # truco)|00000000(mesa)|0(virada)
            self.prepara_mensagem(carta_jogada)
            # envia a mensagem para o servidor..
            print "mensagem para o envio ", self.mensagem_servidor
            self.conexao.envia_mensagem(self.mensagem_servidor)

    def main(self):
        """Realiza a renderização.."""

        pygame.init()

        pygame.display.set_caption("Truco")
        pygame.DOUBLEBUF

        self.gui.iniciar()

        self.carta_selecionada = -1
        select = 0
        # print "Mensagem das Cartas ",self.mensagem_servidor
        while True:

            for event in pygame.event.get():
                self.gui.mostra_pontuacao(self.jogador.equipe)
                self.gui.rodadas(self.jogador.equipe)
                self.atualiza_mensagem()
                self.verifica_proposta_truco()
                self.gui.desenha_botao_truco(
                    self.gui.valor_rodada, self.proposta_truco_equipe)
                if event.type == QUIT:
                    print "Encerrando conexão...."
                    pygame.quit()
                    sys.exit()
                    self.verifica.exit()
                    self.quee.join()
                if event.type == KEYDOWN and self.flag_truco == 0 and self.sua_vez == 1:
                    op = event.unicode
                    print op
                    op = str(op)
                    if op is "":
                        op = str(event.key)
                        print op
                    if op == "1":
                        self.gui.update_card(
                            self.gui.mao[0], self.gui.pos_cartas_jog)
                        self.carta_selecionada = 0
                    if op == "2":
                        self.gui.update_card(
                            self.gui.mao[1], self.gui.pos_cartas_jog)
                        self.carta_selecionada = 1
                    if op == "3":
                        self.gui.update_card(
                            self.gui.mao[2], self.gui.pos_cartas_jog)
                        self.carta_selecionada = 2
                    if (op == "275" or op == "276") and self.rodada is not 1:
                        """Teclas de Seta esq e dir
                            carta oculta
                        """
                        self.gui.update_card(
                            self.gui.mao[3], self.gui.pos_cartas_jog)
                        self.carta_selecionada = 3
                    else:
                        print "Jogada não permitida."
                    if op == "273":
                        print "carta jogada", self.gui.mao[self.carta_selecionada]
                        if (self.carta_selecionada != -1):
                            # self.gui.jogar_carta(
                            # self.gui.mao[self.carta_selecionada],
                            # self.conexao)
                            self.sua_vez = 1  # Bloqueia a mão ..
                            self.envia_carta_servidor(
                                self.gui.mao[self.carta_selecionada])
                            # Update a carta do adversario para teste
                            # Atualiza as cartas em miniatura
                            #---------------------------------------

                            #self.gui.update_card_adversario(1, 1)
                            #self.gui.update_card_adversario(2, 1)
                            #self.gui.update_card_adversario(3, 1)

                            if self.carta_selecionada is not 3:
                                self.gui.mao[self.carta_selecionada] = None
                            self.gui.verifica_mao(self.gui.mao, self.conexao)
                            # self.gui.pause()
                if event.type == MOUSEBUTTONDOWN and select == 0:
                    """Define a mudança da tela"""
                    print event.button, event.pos
                    fundo = pygame.image.load(
                        self.gui.caminho_background + "fundo.jpg")
                    self.gui.novo_tamanho_janela()
                    self.gui.tela.blit(fundo, [0, 0])
                    # self.gui.rodadas()
                    # self.gui.mostra_pontuacao()
                    # self.gui.desenha_botao_truco(self.gui.valor_rodada)

                    self.gui.update_card_adversario(0, 3)
                    self.gui.escrever(
                        "Para selecionar cartas escolha [1,2,3]", (30, 30),
                        self.gui.branco)
                    self.gui.escrever(
                        "Para Jogar a carta utilize seta para frente", (
                            30, 50),
                        self.gui.branco)
                    self.gui.escrever(
                        "Utilize as setas direcionais para ocultar", (30, 70),
                        self.gui.branco)
                    select = 1
                if event.type == MOUSEBUTTONDOWN and self.sua_vez == 1:
                    pos = event.pos
                    print "Posicao ", pos
                    if (pos[0] > 670 and pos[0] < 780):
                        if(pos[1] > 471 and pos[1] < 471 + 20):
                            # self.gui.desenha_botao_truco(self.gui.valor_rodada)
                            if (self.truco_habilitado is 1):
                                print "entrouuu"
                                print "Variaveis do truco Sua Vez ", self.sua_vez, type(self.sua_vez), "Minha equipe ", self.jogador.equipe, type(self.jogador.equipe), "Proposta truco equipe ", self.proposta_truco_equipe, type(self.proposta_truco_equipe)
                                if(self.sua_vez is 1 and (self.jogador.equipe == self.proposta_truco_equipe or self.proposta_truco_equipe == "0")):
                                    print "pedindo truco"
                                    self.pede_truco = "1"
                                    self.solicita_truco()
                                    self.flag_truco = 1
                                else:
                                    print "Não é permitido pedir truco na mão de 12"
                            else:
                                print "A opção de truco não está Habilitada."
                    if (pos[0] > 363 and pos[0] < 392) and self.flag_truco is 1:
                        if (pos[1] > 236 and pos[1] < 276):
                            print "Truco Aceito"
                            self.resposta_proposta_truco = "1"
                            self.responde_truco()
                            self.gui.tela_padrao(self.jogador.equipe)
                            self.flag_truco = 0

                    if (pos[0] > 410 and pos[0] < 441) and self.flag_truco is 1:
                        if (pos[1] > 237 and pos[1] < 266):
                            print "Truco Não Foi aceito"
                            self.gui.tela_padrao(self.jogador.equipe)
                            self.resposta_proposta_truco = "0"
                            se.responde_truco()
                            self.flag_truco = 0
                            # self.cartas_jogadas()

            pygame.display.update()

            for i in range(0, 1):
                # Percorre a fila lendo as mensagens recebidas do servidor
                if not self.quee.empty():
                    retorno = self.quee.get(i)
                    self.processa_resposta(retorno)
                    # Adiciona um evento na pilha de eventos para atualizar a
                    # tela.
                    evento = pygame.event.Event(USEREVENT)
                    pygame.event.post(evento)


if __name__ == '__main__':
    new = Principal()
    new.main()
