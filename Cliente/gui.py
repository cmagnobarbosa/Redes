# coding: utf-8
import pygame
import pygame.gfxdraw
import sys
from pygame.locals import *
import os
import random

# Modulo de conexão
"""
Cliente
Tp de Redes - Truco
UFSJ
Carlos Magno
Lucas Geraldo

Requisitos:
*python 2.7
*pygame

Modulo de GUI.

"""


class Gui():
    """Classe Gui"""

    def __init__(self):
        """A lista da mão deve ser recebida do servidor"""

        self.caminho_cartas = "cartas/"
        self.caminho_background = "background/"
        self.branco = (255, 255, 255)
        #-----------------------------------------
        self.pos_cartas_jog = (400, 400, 66, 90)
        self.sua_pos_carta = (400, 270, 66, 90)
        self.pos_cartas_jog_3 = (266, 170, 66, 90)
        self.pos_cartas_jog_2 = (400, 70, 66, 90)
        self.pos_cartas_jog_1 = (534, 170, 66, 90)

        #-----------------------------------------
        self.lista_cards = []
        self.cartas_recebidas = []
        self.mao = []
        #-----------------------
        self.valor_rodada = "0"
        self.pontos = "0000"
        self.partidas="000"
        self.mensagem_vez="Aguarde..."
        #---------------------

        self.tela = pygame.display.set_mode((500, 400), 0, 32)
        self.icone = pygame.image.load("expresso.png")
        pygame.display.set_icon(self.icone)

    def atualiza_pontuacao(self, ponto):
        self.valor_rodada = ponto

    def desenha_botao_truco(self, texto):
        """Desenha o Botão de truco"""
        pygame.draw.rect(self.tela, (192, 192, 192), (670, 471, 110, 20))
        self.escrever(texto, (670, 471),self.branco)

    def mostra_pontuacao(self):
        """ Renderiza a Pontuação."""
        #Quadrado do valor da rodada
        pygame.draw.rect(self.tela, (0, 0, 0), (670, 450, 110, 20))

        pygame.draw.rect(self.tela, (0, 0, 0), (29, 450, 145, 20))

        pygame.draw.rect(self.tela,(0, 0, 0),(29,430,145,20))
        self.escrever(self.mensagem_vez,(40,430),(255,0,0))
        self.escrever("Valor Rod: " + self.valor_rodada, (670, 450), self.branco)
        self.escrever("Nós: " + self.pontos[0:2] + " Eles: " +
                      self.pontos[2:4], (40, 450), self.branco)

    def rodadas(self):
        """"Desenha um bloco"""

        card = pygame.draw.rect(self.tela, (0, 0, 0), (29, 471, 145, 30))
        self.escrever("[" + self.partidas[0:1] + "] | [" + self.partidas[1:2] +
                      "] | [" + self.partidas[2:3] + "]", (40, 471),self.branco)
        pygame.display.update()

    def carrega_cartas(self):
        """Carrega o caminho das imagens recebidas do servidor"""
        for i in range(0, 3):
            self.mao.append(self.caminho_cartas +
                            self.cartas_recebidas[i] + ".png")
        self.mao.append(self.caminho_cartas + "vv.png")

    def update_card(self, card, posicao):
        """Atualiza o desenho das cartas"""
        """(posicao_horizontal,posicao_vertical,d_altura,d_largura)"""
        if card is not None:
            card = pygame.image.load(card)
            #(X,Y,Largura,Altura)
            self.tela.blit(card, posicao)

    def update_card_adversario(self, jogador, carta):
        """Essa função atualiza a exibição do verso da carta dos adversários"""
        """ O valor jogador 0 é o estado inicial"""
        print "Carta ", carta, "Jogador ", jogador
        if carta is not None:
            if carta is 3:
                carta = self.caminho_cartas + "/miniatura/3_cards.png"
            if carta is 2:
                carta = self.caminho_cartas + "/miniatura/2_cards.png"
            if carta is 1:
                carta = self.caminho_cartas + "/miniatura/1_card.png"
            card = pygame.image.load(carta)

            if jogador is 3 or jogador is 0:
                self.tela.blit(card, (4, 212, 54, 43))

            if jogador == 2 or jogador is 0:
                #(X,Y,Largura,Altura)
                card = pygame.transform.rotate(card, -90)
                self.tela.blit(card, (400, 2, 54, 43))

            if jogador == 1 or jogador is 0:
                card = pygame.image.load(carta)
                card = pygame.transform.rotate(card, 180)
                self.tela.blit(card, (750, 212, 54, 43))

    def verifica_mao(self, mao, conexao):
        """Verifica a mão e encerra a conexao com o servidor"""
        cont = 0
        for i in mao:
            if i is None:
                cont = cont + 1
        if cont >= 3:
            print("Fim de rodada")
            #conexao.envia_mensagem("Fim")
            #conexao.encerra_conexao()

    def renderiza_cartas_jogadas(self, carta_jogada, posicao):
        """Renderiza a carta jogada"""
        self.update_card(carta_jogada, posicao)

    def jogar_carta(self, carta, conexao):
        """Desenha a cart que foi jogada"""
        if carta is not None:
            card = pygame.image.load(carta)
            card_rect = card.get_rect()
            # (Largura)
            self.tela.blit(card, self.sua_pos_carta)
            return 1

    def iniciar(self):
        """Tela inicial"""
        myfont = pygame.font.SysFont("arial", 30)
        label = myfont.render(
            "Clique Para Iniciar o jogo!", 1, (255, 255, 255))
        truco = pygame.image.load("background/background.png")
        self.tela.blit(truco, (0, 0))
        self.tela.blit(label, (120, 370))

    def novo_tamanho_janela(self):
        "Largura x Altura"
        self.tela = pygame.display.set_mode((800, 500), 0, 32)

    def escrever(self, texto, posicao , cor ):
        """Formato posicao (horizontal,vertical)"""
        texto_c = unicode(texto, "utf-8")
        myfont = pygame.font.SysFont("arial", 18)
        label = myfont.render(texto_c, 1, cor)
        #(X,y)
        self.tela.blit(label, posicao)

    def tela_padrao(self):
        fundo = pygame.image.load("background/fundo.jpg")
        self.tela.blit(fundo, [0, 0])
        self.rodadas()
        self.mostra_pontuacao()
        self.desenha_botao_truco("Truco")
        self.update_card_adversario(0, 3)
        self.escrever(
            "Para selecionar cartas escolha [1,2,3]", (30, 30),self.branco)
        self.escrever(
            "Para Jogar a carta utilize seta para frente", (30, 50),self.branco)
        self.escrever(
            "Utilize as setas direcionais para ocultar", (30, 70),self.branco)
        # self.tela.blit(truco,(200,170,450,100))

    def tela_truco(self):
        """Renderiza a tela de Truco e retorna a resposta"""
        truco = pygame.image.load("truco.png")
        tamanho = pygame.Surface.get_rect(truco)
        self.tela.blit(truco, (200, 170, 450, 100))
        # truco.fill((0,0,0,0))
        # truco.set_alpha(255)

        # print type(truco)

        # 0,0,0,0 clear..
        # pygame.gfxdraw.box(self.tela, pygame.Rect(427,204,65,60), (192,192,192,192))
        # self.escrever("TRUCO",(427,204))
        # self.escrever("",(427,204))

    def pause(self):
        print "Jogo pausado Aguarde..."
        pygame.time.delay(4000)
        print "Fim do pause.."
