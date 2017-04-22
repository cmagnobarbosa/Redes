#coding: utf-8
import pygame, sys
from pygame.locals import *
import os
lista_cards = []

def carrega_cartas():
    """Carrega as imagens das cartas"""
    diretorio_cartas="cartas/"
    for naipe_cards in os.listdir(diretorio_cartas):
        if (".png") in naipe_cards:
            lista_cards.append(naipe_cards)

def carrega_uma_carta(nome):
    """O nome deve possuir a extensão"""
    for i in lista_cards:
        if nome == i:
            return "cartas/"+nome
def update_card(tela,card):
    card_king = pygame.image.load(card)
    king_rect = card_king.get_rect()
    tela.blit(card_king,(200, 152, 172, 250))

def jogar_carta(tela,carta):
    card_king = pygame.image.load(carta)
    king_rect = card_king.get_rect()
    tela.blit(card_king,(10, 10, 172, 250))

def iniciar(tela,cor):
    myfont = pygame.font.SysFont("arial", 30)
    # render text
    label = myfont.render("Clique Para Iniciar o jogo!", 1,(255,255,255))
    truco = pygame.image.load("background.png")
    tela.blit(truco,(0,0))
    tela.blit(label, (120, 370))

def main():
    carrega_cartas()
    print lista_cards
    pygame.init()

    tela=pygame.display.set_mode((500,400),0,32)
    pygame.display.set_caption("Truco")
    pygame.DOUBLEBUF
    WHITE=(255,255,255)
    blue=(0,0,255)
    gray = (128,128,128)
    tela.fill(WHITE)
    icone = pygame.image.load("expresso.png")
    pygame.display.set_icon(icone)
    iniciar(tela,blue)
    carta_selecionada = ""
    select=0

    while True:
        for event in pygame.event.get():
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                op= event.unicode
                op = str(op)
                if op is "":
                    op=str(event.key)
                if op == "1":
                    update_card(tela,"cartas/zap.png")
                    carta_selecionada = "cartas/zap.png"
                if op == "2":
                    update_card(tela,"cartas/7_of_diamonds.png")
                    carta_selecionada = "cartas/7_of_diamonds.png"
                if op == "3":
                    update_card(tela,"cartas/king_of_hearts2.png")
                    carta_selecionada = "cartas/king_of_hearts2.png"
                if op == "273":
                    print "carta jogada"
                    jogar_carta(tela,carta_selecionada)

            if event.type== MOUSEBUTTONDOWN and select==0:
                print event.button, event.pos
                fundo = pygame.image.load("fundo.jpg")
                tela.blit(fundo,[0,0])
                myfont = pygame.font.SysFont("arial", 18)
                # render text
                texto = "Para selecionar cartas escolha [1,2,3]"
                label = myfont.render(texto, 1,(255,255,255))
                tela.blit(label, (150, 30))
                texto = "Para Jogar a carta utilize seta para frente"
                label = myfont.render(texto, 1,(255,255,255))
                tela.blit(label, (150, 45))
                select=1

        #update_card(tela,None)
        pygame.display.update()
main()
