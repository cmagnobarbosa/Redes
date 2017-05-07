# coding: utf-8
import pygame
import sys
from pygame.locals import *
from gui import *
from conexao import *
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
        self.carta_selecionada=-1
        self.flag_truco=0
        self.rodada=2
        self.conexao = Conexao()
        self.conexao.conectar()
        self.gui = Gui()
        self.gui.recebe_cartas(self.conexao)
        self.gui.carrega_cartas()
        self.flag_carta_jogada=0
        self.flag_next =1


    def verifica_resposta_servidor(self):
        while(True):
            permissao = self.conexao.ler_socket()
            print"Leitura,",permissao
            if permissao == 1:
                return 1

    def main(self):

        pygame.init()


        pygame.display.set_caption("Truco")
        pygame.DOUBLEBUF


        self.gui.iniciar()

        self.carta_selecionada = -1
        select = 0

        while True:

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == KEYDOWN and self.flag_truco==0 and self.flag_carta_jogada==0:
                    op = event.unicode
                    print op
                    op = str(op)
                    if op is "":
                        op = str(event.key)
                        print op
                    if op == "1":
                        self.gui.update_card(self.gui.mao[0], self.gui.pos_cartas_jog)
                        self.carta_selecionada = 0
                    if op == "2":
                        self.gui.update_card(self.gui.mao[1], self.gui.pos_cartas_jog)
                        self.carta_selecionada = 1
                    if op == "3":
                        self.gui.update_card(self.gui.mao[2], self.gui.pos_cartas_jog)
                        self.carta_selecionada = 2
                    if (op == "275" or op == "276") and self.rodada is not 1:
                        """Teclas de Seta esq e dir
                            carta oculta
                        """
                        self.gui.update_card(self.gui.mao[3], self.gui.pos_cartas_jog)
                        self.carta_selecionada = 3
                    else:
                        print "Jogada não permitida."
                    if op == "273":
                        print "carta jogada", self.gui.mao[self.carta_selecionada]
                        if (self.carta_selecionada != -1):
                            self.flag_carta_jogada= self.gui.jogar_carta(self.gui.mao[self.carta_selecionada],self.conexao)
                            # Update a carta do adversario para teste
                            # Atualiza as cartas em miniatura
                            #---------------------------------------
                            self.gui.update_card_adversario(1, 1)
                            self.gui.update_card_adversario(2, 1)
                            self.gui.update_card_adversario(3, 1)
                            #---------------------------------------
                            # Renderiza as cartas que foram jogadas
                            #---------------------------------------
                            self.gui.renderiza_cartas_jogadas(
                                self.gui.mao[self.carta_selecionada], self.gui.pos_cartas_jog_1)
                            self.gui.renderiza_cartas_jogadas(
                                self.gui.mao[self.carta_selecionada], self.gui.pos_cartas_jog_2)
                            self.gui.renderiza_cartas_jogadas(
                                self.gui.mao[self.carta_selecionada], self.gui.pos_cartas_jog_3)
                            #--------------------------------------
                            if self.carta_selecionada is not 3:
                                self.gui.mao[self.carta_selecionada]=None
                            self.gui.verifica_mao(self.gui.mao,self.conexao)
                            #self.gui.pause()
                if event.type == MOUSEBUTTONDOWN and select == 0 and self.flag_carta_jogada==0:
                    """Define a mudança da tela"""
                    print event.button, event.pos
                    fundo = pygame.image.load(
                        self.gui.caminho_background + "fundo.jpg")
                    self.gui.novo_tamanho_janela()
                    self.gui.tela.blit(fundo, [0, 0])
                    self.gui.rodadas()
                    self.gui.mostra_pontuacao()
                    self.gui.desenha_botao_truco("Truco")

                    self.gui.update_card_adversario(0, 3)
                    self.gui.escrever(
                        "Para selecionar cartas escolha [1,2,3]", (30, 30))
                    self.gui.escrever(
                        "Para Jogar a carta utilize seta para frente", (30, 50))
                    self.gui.escrever(
                        "Utilize as setas direcionais para ocultar", (30, 70))
                    select = 1
                if event.type == MOUSEBUTTONDOWN and self.flag_carta_jogada==0:
                    pos = event.pos
                    print "Posicao ", pos
                    if (pos[0] > 700 and pos[0] < 750):
                        if(pos[1] > 471 and pos[1] < 471 + 20):
                            self.gui.desenha_botao_truco("Seis")
                            self.gui.tela_truco()
                            self.flag_truco = 1
                    if (pos[0]> 363 and pos[0] < 392) and self.flag_truco is 1:
                        if (pos[1]> 236 and pos[1] < 276):
                            print "Truco Aceito"
                            self.gui.tela_padrao()
                            #self.main()
                            self.flag_truco =0
                            #self.cartas_jogadas()
                    if (pos[0]>410 and pos[0]<441) and self.flag_truco is 1:
                        if (pos[1] > 237 and pos[1]< 266):
                            print "Truco Não Foi aceito"
                            self.gui.tela_padrao()
                            self.flag_truco = 0
                            #self.cartas_jogadas()


            # update_card(tela,None)
            pygame.display.update()
            if self.flag_carta_jogada is 1:
                self.flag_carta_jogada=self.verifica_resposta_servidor()

if __name__ == '__main__':
    new = Principal()
    new.main()
