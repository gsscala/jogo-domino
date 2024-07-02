from basic_players import Player
import random




class jovane(Player):

    def __init__(self):
        super().__init__(281210, "cebola")

    def info(self, historico, posicao, extremos):
        # ver que na real eu posso contabilizar as peças que ja foram jogadas com as que eu tenho para descobrir quais peças ninguem alem de mim tem
        global extremidades
        global pecas
        extremidades = []
        for peca in [
            peca_[1] for peca_ in historico if not peca_[3] and peca_[0] % 2 != posicao % 2
        ]:
            extremidades.append(peca[0][0])
            extremidades.append(peca[1][1])
        jogadas_bloqueadoras = []
        for peca in self._tiles:
            for extremidade in extremidades:
                if extremidade == peca[0]:
                    if peca[1] == extremos[0]:
                        jogadas_bloqueadoras.append(0, peca)
                    if peca[1] == extremos[1]:
                        jogadas_bloqueadoras.append(1, (peca[1], peca[0]))
                if extremidade == peca[1]:
                    if peca[0] == extremos[0]:
                        jogadas_bloqueadoras.append(0, (peca[1], peca[0]))
                    if peca[0] == extremos[1]:
                        jogadas_bloqueadoras.append(1, peca)
        pecas = sorted([peca for peca in self._tiles if peca[0] == peca[1]], key = lambda x: (x[0] + x[1]), reverse=True) + sorted(self._tiles, key = lambda x: (x[0] + x[1]), reverse=True)
        for peca in pecas:
            if extremos[0] == peca[0]:
                peca = 0, (peca[1], peca[0])
            elif extremos[0] == peca[1]:
                peca = 0, peca
            elif extremos[1] == peca[0]:
                peca = 1, peca
            elif extremos[1] == peca[1]:
                peca = 1, (peca[1], peca[0])
            else:
                pecas.remove(peca)
        pecas = sorted(jogadas_bloqueadoras, key = lambda x: (x[1][0] + x[1][1]), reverse = True) + pecas

    def play(self, board_extremes, play_hist):
        if len(play_hist) == 0:
            return random.randint(0, 1), (sorted([peca for peca in self._tiles if peca[0] == peca[1]], key = lambda x: (x[0] + x[1]), reverse=True) + sorted(self._tiles, key = lambda x: (x[0] + x[1]), reverse=True))[0] 
        jovane.info(self, play_hist, jovane.position, board_extremes)
        print(pecas)
        if board_extremes[0] in extremidades:
            for jogada in pecas: #colocar isso no começo da lista de peças
                if jogada[0] == 1:
                    return jogada # se nao tiver nada jogar a melhor na direita
        if board_extremes[1] in extremidades:
            for jogada in pecas: #colocar isso no começo da lista de peças
                if jogada[0] == 0:
                    return jogada # se nao tiver nada jogar a melhor na esquerda
        return pecas[0]
