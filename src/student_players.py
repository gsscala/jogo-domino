from basic_players import Player

# Implemente neste arquivo seus jogadores

# Jogador que não faz nada. Subsitua esta classe pela(s) sua(s), ela(s) deve(m) herdar da classe Player
class NonePLayer(Player):

    def __init__(self):
        super().__init__(0, "Ninguém")

    def play(self, board_extremes, play_hist):
        return 1, None
		
# Função que define o nome da dupla:
def pair_name():
    return "algum nome" # Defina aqui o nome da sua dupla

# Função que cria a dupla:
def create_pair():
    return (NonePLayer(), NonePLayer()) # Defina aqui a dupla de jogadores. Deve ser uma tupla com dois jogadores.	
