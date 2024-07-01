from basic_players import Player
import random


def info(historico, posicao):
    # ver que na real eu posso contabilizar as peças que ja foram jogadas com as que eu tenho para descobrir quais peças ninguem alem de mim tem
    global pecas
    global pecas_boas
    global extremidade_esquerda
    global extremidade_direita
    global jogadas_possiveis
    pecas = sorted(
        [peca for peca in Player.tiles if peca[0] == peca[1]], key = lambda x: (x[0] + x[1], 0), reverse=True
    ).extend(
        sorted(Player.tiles, key = lambda x: (x[0] + x[1], 0) reverse=True)
    )  # ordenar pelo somatorio #dar um jeito de não repetir as pecas
    pecas_boas = [
        peca[1] for peca in historico if not peca[3] and peca[0] % 2 != posicao % 2
    ]
    extremidade_esquerda = []
    extremidade_direita = []
    for peca in pecas_boas:
        peca[0] = peca[0][0]
        extremidade_esquerda.append(peca[0][0])
        peca[1] = peca[1][1]
        extremidade_direita.append(peca[1][1])
    for peca in pecas_boas:
        for peca_ in pecas:
            if peca[0] in peca_ or peca[1] in peca_:
                pecas_legais.append()
    jogadas_possiveis = []
    for peca in pecas:
        for extremidade in extremidade_esquerda:
            if extremidade in peca:
                jogadas_possiveis.append(0, peca)  # ajustar orientacao da peca
        for extremidade in extremidade_direita:
            if extremidade in peca:
                jogadas_possiveis.append(1, peca)  # ajustar orientacao da peca


class jovane(Player):

    def __init__(self):
        super().__init__(281210, "cebola")

    def play(self, board_extremes, play_hist):
        info(play_hist, jovane.position)
        if board_extremes == ():
            return random.randint(0, 1), pecas[0]
        if board_extremes[0] in extremidade_esquerda:
            for jogada in jogadas_possiveis:
                if jogada[0] == 1:
                    return jogada # se nao tiver nada jogar a melhor na direita
        if board_extremes[1] in extremidade_direita:
            for jogada in jogadas_possiveis:
                if jogada[0] == 0:
                    return jogada # se nao tiver nada jogar a melhor na esquerda
        return 1, None  # pecas[0] se tiver como
