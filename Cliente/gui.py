# coding: utf-8
import pygame
import sys
from pygame.locals import *
import os
import random
"""
Cliente
Tp de Redes - Truco
UFSJ
Carlos Magno
Lucas Geraldo

Requisitos:
*python 2.7
*pygame

"""


class Gui:
    """Classe Gui"""

    def __init__(self):
        """A lista da mão deve ser recebida do servidor"""
        self.lista_cards = []
        self.cards_selected = []
        self.mao = []
        self.tela = pygame.display.set_mode((500, 400), 0, 32)
        self.icone = pygame.image.load("expresso.png")
        pygame.display.set_icon(self.icone)

    def desenha_botao_truco(self):
        """Desenha o Botão de truco"""
        valor="Truco"
        pygame.draw.rect(self.tela,(192,192,192),(700,471, 50,20))
        self.escrever(valor,(700,471))
        #card = pygame.draw.rect(janela, (0, 0, 0), (723, 432, 350, 30))

    def mostra_pontuacao(self):
        """ Renderiza a Pontuação."""
        ponto = 0
        ponto_ad = 0
        self.escrever("Nós: "+str(ponto)+" Eles: "+str(ponto_ad),(40,450))

    def rodadas(self):
        """"Desenha um bloco"""
        p_1=" V "
        p_2=" X "
        p_3=" - "
        card = pygame.draw.rect(self.tela, (0, 0, 0), (29, 471, 350, 30))
        self.escrever("["+str(p_1)+"] | ["+str(p_2)+"] | ["+str(p_3)+"]",(40,471))
        pygame.display.update()

    def distribui_cartas(self):
        """Função de teste.. as cartas devem ser recebidas do servidor"""
        self.cards_selected[:] = []
        for k in range(0, 3):
            valor = random.randint(0, len(self.lista_cards) - 1)
            if valor in self.cards_selected:
                self.distribui_cartas()
            self.cards_selected.append(valor)

    def carrega_cartas(self):
        """Carrega as imagens das cartas"""
        diretorio_cartas = "cartas/"
        for naipe_cards in os.listdir(diretorio_cartas):
            if (".png") in naipe_cards:
                self.lista_cards.append(naipe_cards)

    def update_card(self, card):
        """Atualiza o desenho das cartas"""
        """(posicao_horizontal,posicao_vertical,d_altura,d_largura)"""
        card = pygame.image.load(card)
        card_rect = card.get_rect()
        self.tela.blit(card, (400, 250, 172, 250))

    def jogar_carta(self, carta):
        """Desenha a cart que foi jogada"""
        card_king = pygame.image.load(carta)
        king_rect = card_king.get_rect()
        self.tela.blit(card_king, (10, 10, 172, 250))

    def iniciar(self, cor):
        """Tela inicial"""
        myfont = pygame.font.SysFont("arial", 30)
        label = myfont.render(
            "Clique Para Iniciar o jogo!", 1, (255, 255, 255))
        truco = pygame.image.load("background/background.png")
        self.tela.blit(truco, (0, 0))
        self.tela.blit(label, (120, 370))

    def gera_mao(self):
        """Gera a mão a partir das listas de cartas selecionadas"""
        for i in self.cards_selected:
            print "Valor de I", i, "Tamanho ", len(self.lista_cards)
            self.mao.append("cartas/" + self.lista_cards[i])
        self.mao.append("cartas/verso2.jpg")

    def novo_tamanho_janela(self):
        self.tela = pygame.display.set_mode((800, 500), 0, 32)

    def escrever(self, texto, posicao):
        """Formato posicao (horizontal,vertical)"""
        texto_c = unicode(texto,"utf-8")
        myfont = pygame.font.SysFont("arial", 18)
        label = myfont.render(texto_c, 1, (255, 255, 255))
        self.tela.blit(label, posicao)

    def monitora_clique(horizontal,ver):
        pass

    def main(self):
        self.carrega_cartas()
        self.distribui_cartas()
        self.gera_mao()

        pygame.init()

        pygame.display.set_caption("Truco")
        pygame.DOUBLEBUF
        WHITE = (255, 255, 255)
        blue = (0, 0, 255)
        gray = (128, 128, 128)
        self.tela.fill(WHITE)

        self.iniciar(blue)

        carta_selecionada = -1
        select = 0

        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN:
                    op = event.unicode
                    print op
                    op = str(op)
                    if op is "":
                        op = str(event.key)
                        print op
                    if op == "1":
                        self.update_card(self.mao[0])
                        carta_selecionada = 0
                    if op == "2":
                        self.update_card(self.mao[1])
                        carta_selecionada = 1
                    if op == "3":
                        self.update_card(self.mao[2])
                        carta_selecionada = 2
                    if op == "275" or op == "276":
                        """Teclas de Seta esq e dir
                            carta oculta
                        """
                        print "Entrouu", self.mao[3]
                        self.update_card(self.mao[3])
                        carta_selecionada = 3
                    if op == "273":
                        print "carta jogada", self.mao[carta_selecionada]
                        if (carta_selecionada != -1):
                            self.jogar_carta(self.mao[carta_selecionada])

                if event.type == MOUSEBUTTONDOWN and select ==0:
                    """Define a mudança da tela"""
                    print event.button, event.pos
                    fundo = pygame.image.load("background/fundo2.jpg")
                    self.novo_tamanho_janela()
                    self.tela.blit(fundo, [0, 0])
                    self.rodadas()
                    self.mostra_pontuacao()
                    self.desenha_botao_truco()
                    self.escrever(
                        "Para selecionar cartas escolha [1,2,3]", (400, 30))
                    self.escrever(
                        "Para Jogar a carta utilize seta para frente", (400, 50))
                    self.escrever(
                        "Utilize as setas direcionais para ocultar", (400, 70))
                    select = 1
                if event.type == MOUSEBUTTONDOWN:
                    pos = event.pos
                    if (pos[0]>700 and pos[0]<750):
                        if(pos[1]>471 and pos[1]<471+20):
                            print "Truco"


            # update_card(tela,None)
            pygame.display.update()
if __name__ == '__main__':
    newgui = Gui()
    newgui.main()
