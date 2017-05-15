# coding: utf-8

class Jogador:
    """Vai armazenar os dados do jogador"""
    def __init__(self):
        self.id=""
        self.equipe=""
        self.cartas_mao = ""

    def update(self,id_jogo,equipe,cartas_mao):
        self.id=id_jogo
        self.equipe=equipe
        self.cartas_mao=cartas_mao
