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
        self.mensagem_servidor = "A"
        self.carta_selecionada = -1
        self.flag_truco = 0
        self.rodada = 2
        self.conexao = Conexao()
        self.conexao.conectar()
        self.gui = Gui()
        self.jogador = Jogador()
        self.recebe_cartas()
        self.gui.carrega_cartas()
        self.sua_vez = 0
        self.quee = Queue()
        self.flag_next = 1
        self.gui.valor_rodada = "0"

        self.verifica = Thread(target=self.verifica_resposta_servidor, args=(
            self.quee, self.conexao))
        self.verifica.daemon = True
        self.verifica.start()

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
        """ Possui o socket de conexão como parametro de entrada."""
        """Carrega as cartas recebidas do servidor"""
        self.conexao.envia_mensagem("0")
        self.mensagem_servidor = self.conexao.ler_socket()
        print "Me", self.mensagem_servidor
        #--Extrai os dados iniciais...
        self.jogador.id = self.mensagem_servidor[0:1]
        self.jogador.equipe = self.mensagem_servidor[1:2]
        self.sua_vez = self.mensagem_servidor[2:3]
        cartas = self.mensagem_servidor[4:10]
        self.jogador.cartas_mao = cartas
        # print "ID",ID,"Equipe ",equipe, "Mão ",mao

        cartas = self.agrupa_cartas(cartas)
        for i in cartas:
            self.gui.cartas_recebidas.append(i)

    def verifica_resposta_servidor(self, fila, conexao):
        """Verifica a conexao.."""
        while (True):
            palavra = conexao.ler_socket()
            self.quee.put(palavra)

    def processa_resposta(self, lista):
        """Vai processar a mensagem recebida"""
        #self.mensagem_servidor= lista
        print "resposta ", lista
        print lista[2:3]
        self.sua_vez = int(lista[2:3])
        print self.sua_vez

    def prepara_mensagem(self, carta_jogada):
        """Prepara uma mensagem para o envio"""
        print "Mensagem ", self.mensagem_servidor
        # acerta o id
        self.mensagem_servidor = self.mensagem_servidor[
            :0] + self.jogador.id + self.mensagem_servidor[1:]
        # Acerta a equipe
        self.mensagem_servidor = self.mensagem_servidor[
            :1] + self.jogador.equipe + self.mensagem_servidor[2:]
        # Acera a posicao da carta na mesa
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

    def envia_carta_servidor(self, carta_jogada):
        """Dispara cartas para o servidor"""
        print "Self Mensagem", self.mensagem_servidor
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
                self.gui.mostra_pontuacao()
                self.gui.rodadas()
                if event.type == QUIT:
                    print "Encerrando conexão...."
                    pygame.quit()
                    sys.exit()
                    self.verifica.exit()
                    self.quee.join()
                if event.type == KEYDOWN and self.flag_truco == 0 and self.sua_vez == 0:
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
                            self.gui.jogar_carta(
                                self.gui.mao[self.carta_selecionada], self.conexao)
                            self.sua_vez = 1  # Bloqueia a mão ..
                            self.envia_carta_servidor(
                                self.gui.mao[self.carta_selecionada])
                            # Update a carta do adversario para teste
                            # Atualiza as cartas em miniatura
                            #---------------------------------------
                            self.gui.update_card_adversario(1, 1)
                            #self.gui.update_card_adversario(2, 1)
                            #self.gui.update_card_adversario(3, 1)

                            #---------------------------------------
                            # Renderiza as cartas que foram jogadas
                            #---------------------------------------
                            self.gui.renderiza_cartas_jogadas(
                                self.gui.mao[self.carta_selecionada], self.gui.pos_cartas_jog_1)
                            # self.gui.renderiza_cartas_jogadas(
                            #     self.gui.mao[self.carta_selecionada], self.gui.pos_cartas_jog_2)
                            # self.gui.renderiza_cartas_jogadas(
                            #     self.gui.mao[self.carta_selecionada], self.gui.pos_cartas_jog_3)
                            #--------------------------------------
                            if self.carta_selecionada is not 3:
                                self.gui.mao[self.carta_selecionada] = None
                            self.gui.verifica_mao(self.gui.mao, self.conexao)
                            # self.gui.pause()
                if event.type == MOUSEBUTTONDOWN and select == 0 and self.sua_vez == 0:
                    """Define a mudança da tela"""
                    print event.button, event.pos
                    fundo = pygame.image.load(
                        self.gui.caminho_background + "fundo.jpg")
                    self.gui.novo_tamanho_janela()
                    self.gui.tela.blit(fundo, [0, 0])
                    # self.gui.rodadas()
                    # self.gui.mostra_pontuacao()
                    self.gui.desenha_botao_truco("Truco")

                    self.gui.update_card_adversario(0, 3)
                    self.gui.escrever(
                        "Para selecionar cartas escolha [1,2,3]", (30, 30))
                    self.gui.escrever(
                        "Para Jogar a carta utilize seta para frente", (30, 50))
                    self.gui.escrever(
                        "Utilize as setas direcionais para ocultar", (30, 70))
                    select = 1
                if event.type == MOUSEBUTTONDOWN and self.sua_vez == 0:
                    pos = event.pos
                    print "Posicao ", pos
                    if (pos[0] > 700 and pos[0] < 750):
                        if(pos[1] > 471 and pos[1] < 471 + 20):
                            self.gui.desenha_botao_truco("Seis")
                            self.gui.tela_truco()
                            self.flag_truco = 1
                    if (pos[0] > 363 and pos[0] < 392) and self.flag_truco is 1:
                        if (pos[1] > 236 and pos[1] < 276):
                            print "Truco Aceito"
                            self.gui.tela_padrao()
                            # self.main()
                            self.flag_truco = 0
                            # self.cartas_jogadas()
                    if (pos[0] > 410 and pos[0] < 441) and self.flag_truco is 1:
                        if (pos[1] > 237 and pos[1] < 266):
                            print "Truco Não Foi aceito"
                            self.gui.tela_padrao()
                            self.flag_truco = 0
                            # self.cartas_jogadas()

            # update_card(tela,None)
            pygame.display.update()
            # self.gui.valor_rodada="6"
            for i in range(0, 1):
                # Percorre a fila lendo as mensagens recebidas do servidor
                if not self.quee.empty():
                    retorno = self.quee.get(i)
                    self.processa_resposta(retorno)


if __name__ == '__main__':
    new = Principal()
    new.main()
