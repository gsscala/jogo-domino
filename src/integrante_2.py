from basic_players import Player
import random

class giovanni(Player):

    def __init__(self):
        super().__init__(281210, "giovanni", image_path="img/giovanni.jpeg")

    def info(self, historico, posicao, extremos):
        extremidades = []
        for extremidade in [
            peca[1] for peca in historico if not peca[3] and peca[0] % 2 != posicao % 2
        ]:
            extremidades.append(extremidade[0])
            extremidades.append(extremidade[1])
        jogadas_bloqueadoras = []
        for peca in self._tiles:
            for extremidade in extremidades:
                if extremidade == peca[0]:
                    if peca[1] == extremos[0]:
                        jogadas_bloqueadoras.append((0, peca))
                    if peca[1] == extremos[1]:
                        jogadas_bloqueadoras.append((1, peca))
                if extremidade == peca[1]:
                    if peca[0] == extremos[0]:
                        jogadas_bloqueadoras.append((0, peca))
                    if peca[0] == extremos[1]:
                        jogadas_bloqueadoras.append((1, peca))
        pecas = []
        for peca in self._tiles:
            if extremos[0] in peca:
                pecas.append((0, peca))
            elif extremos[1] in peca:
                pecas.append((1, peca))
        pecas = sorted([peca for peca in pecas if peca[0] == peca[1]], key = lambda x: (x[1][0] + x[1][1]), reverse=True) + sorted(pecas, key = lambda x: (x[1][0] + x[1][1]), reverse=True)
        pecas = sorted(jogadas_bloqueadoras, key = lambda x: (x[1][0] + x[1][1]), reverse = True) + pecas
        return pecas, extremidades

    def play(self, board_extremes, play_hist):
        if len(play_hist) == 0:
            pecas = sorted([peca for peca in self._tiles if peca[0] == peca[1]], key = lambda x: (x[0] + x[1]), reverse=True) + sorted(self._tiles, key = lambda x: (x[0] + x[1]), reverse=True)
            return random.randint(0, 1), pecas[0]
        pecas, extremidades = self.info(play_hist, self._position, board_extremes)
        for peca in pecas:
            if board_extremes[0] in extremidades and peca[0] == 1:
                return peca
            if board_extremes[1] in extremidades and peca[0] == 0:
                return peca
        for peca in pecas:
            if set(board_extremes) & set(peca[1]):
                return peca
        return 1, None
