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
        self.mao=[]
        self.tela = pygame.display.set_mode((500, 400), 0, 32)
        self.icone = pygame.image.load("expresso.png")
        pygame.display.set_icon(self.icone)

    def desenha_bloco(self):
        """"Desenha um bloco"""
        print "entrouu"
        janela = pygame.display.get_surface()
        print janela
        pygame.draw.rect(janela,(0,0,255),(350,230,200,200))

    def distribui_cartas(self):
        """Função de teste.. as cartas devem ser recebidas do servidor"""
        self.cards_selected[:]=[]
        for k in range(0,3):
            valor = random.randint(0,len(self.lista_cards)-1)
            if valor in self.cards_selected:
                self.distribui_cartas()
            self.cards_selected.append(valor)

    def carrega_cartas(self):
        """Carrega as imagens das cartas"""
        diretorio_cartas = "cartas/"
        for naipe_cards in os.listdir(diretorio_cartas):
            if (".png") in naipe_cards:
                self.lista_cards.append(naipe_cards)

    def update_card(self,card):
        """Atualiza o desenho das cartas"""
        """(posicao_horizontal,posicao_vertical,d_altura,d_largura)"""
        card= pygame.image.load(card)
        card_rect = card.get_rect()
        self.tela.blit(card, (400, 250, 172, 250))

    def jogar_carta(self,carta):
        """Desenha a cart que foi jogada"""
        card_king = pygame.image.load(carta)
        king_rect = card_king.get_rect()
        self.tela.blit(card_king, (10, 10, 172, 250))

    def iniciar(self,cor):
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
            print "Valor de I",i,"Tamanho ",len(self.lista_cards)
            self.mao.append("cartas/"+self.lista_cards[i])
        self.mao.append("cartas/verso2.jpg")

    def novo_tamanho_janela(self):
        self.tela = pygame.display.set_mode((800, 500),0,32)

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
                    if op == "275" or op =="276":
                        """Teclas de Seta esq e dir
                            carta oculta
                        """
                        self.update_card(self.mao[3])
                        carta_selecionada= 3
                    if op == "273":
                        print "carta jogada", self.mao[carta_selecionada]
                        if (carta_selecionada != -1):
                            self.jogar_carta(self.mao[carta_selecionada])

                if event.type == MOUSEBUTTONDOWN and select == 0:
                    """Define a mudança da tela"""
                    print event.button, event.pos
                    fundo = pygame.image.load("background/fundo2.jpg")
                    self.novo_tamanho_janela()
                    self.desenha_bloco()
                    self.tela.blit(fundo, [0, 0])
                    myfont = pygame.font.SysFont("arial", 18)
                    # render text
                    texto = "Para selecionar cartas escolha [1,2,3]"
                    label = myfont.render(texto, 1, (255, 255, 255))
                    self.tela.blit(label, (400, 30))
                    texto = "Para Jogar a carta utilize seta para frente"
                    label = myfont.render(texto, 1, (255, 255, 255))
                    self.tela.blit(label, (400, 45))
                    select = 1

            # update_card(tela,None)
            pygame.display.update()
if __name__ == '__main__':
    newgui = Gui()
    newgui.main()
