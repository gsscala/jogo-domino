import pygame
import random
import sys
from drawer import draw_game, draw_match, draw_podium
from judge import Judge
from basic_players import GreedyPlayer, DummyPlayer
from student_players import pair_name, create_pair

# Classe que acumula o placar de uma dupla
class Score:

    def __init__(self, pair_name):
        self._pair_name = pair_name
        self._game = [0] * 3
        self._match = [0] * 3

    @property
    def pair_name(self):
        return self._pair_name

    @property
    def match_wins(self):
        return self._match[0]
		
    @property
    def match_ties(self):
        return self._match[1]
		
    @property
    def match_losses(self):
        return self._match[2]

    @property
    def wins(self):
        return self._game[0]
		
    @property
    def ties(self):
        return self._game[1]
		
    @property
    def losses(self):
        return self._game[2]
		
    def _update_score(self, wins = 0, ties = 0, losses = 0):
        self._game[0] += wins
        self._game[1] += ties
        self._game[2] += losses

    def new_match_win(self, wins = 1, ties = 0, losses = 0):
        self._match[0] += 1
        self._update_score(wins, ties, losses)

    def new_match_tie(self, wins = 0, ties = 1, losses = 0):
        self._match[1] += 1
        self._update_score(wins, ties, losses)

    def new_match_losse(self, wins = 0, ties = 0, losses = 1):
        self._match[2] += 1
        self._update_score(wins, ties, losses)

    @property		
    def sorting_attribute(self):
        return self._match + self._game
		
    def __str__(self):
        return f"{self._pair_name} - MATCH[{self._match[0]} WINS, {self._match[1]} TIES, {self._match[2]} LOSSES] - GAMES[{self._game[0]} WINS, {self._game[1]} TIES, {self._game[2]} LOSSES]"

# Duplas do torneio			
PAIRS = {
        'Greedies': (DummyPlayer(1, "Mr Burns", "img/Mr_Burns.jpg"), DummyPlayer(2, "Mr Krabs", "img/Mr_Krabs.jpeg")), 
        'Mixed': (GreedyPlayer(3, "Scrooge McDuck", "img/Scrooge_McDuck.jpg"), GreedyPlayer(4, "Homer_Simpson", "img/Homer_Simpson.png")), 
        'Dummies': (GreedyPlayer(5, "Patrick Star", "img/Patrick_Star.jpeg"), DummyPlayer(6, "Philip Fry", "img/Philip_Fry.jpg")),
		pair_name(): create_pair()
    }
		
# Inicializa pygame
pygame.init()


# Executa um jogo
def play_game(judge, players, speed, first):	
    # Inicia o jogo
    judge.start_game(players, first)
    # Desenha o tabuleiro uma primeira vez
    draw_game(judge.start, judge.board, players)
    # Aguarda
    pygame.time.wait(int(speed))
    # Laço do jogo
    while not judge.ended:
        # Joga
        judge.play()
        # Desenha o tabuleiro
        draw_game(judge.start, judge.board, players)
        # Aguarda
        pygame.time.wait(int(speed))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
    #retorna o ganhador da partida
    return judge.winner()				

				
# Executa uma série de jogos entre uma dupla
def run_match(judge, pair1, pair2, number, speed):	
    # define os jogadores
    players = [pair1[0], pair2[0], pair1[1], pair2[1]]
    # Informa as posições
    for i in range(len(players)):
        players[i].position = i
    # Partidas ganhas por cada dupla
    wins = [0] * 2
    # Define o primeiro jogador
    first = random.randint(0, 3)
    # Executa as partidas
    for i in range(number):
        print(f"--Initializing game: {i+1}")
        winner = play_game(judge, players, speed, first)
        if winner is None:
            print(f"--Finalizing game: {i+1}. Result: tie!")
        else:
            wins[winner] += 1
            print(f"--Finalizing game: {i+1}. Result: {players[winner % 2].name + ' and ' + players[2 + winner % 2].name} WINS!")
        first = (first + 1) % 4
    return wins
    
# Executa o torneio
def run_tournament(number, speed, waiting):
    # Cria o juiz
    judge = Judge()
    # Associa as imagens aos jogadores
    for pair in PAIRS.values():
        for player in pair:
            image = pygame.image.load(player.image_path)
            image = pygame.transform.scale(image, (100, 100))
            player.image = image
    # Cria o placar de cada dupla
    scores = []
    for key in PAIRS:
        scores.append(Score(key))
    # Executa jogos entre cada par de duplas
    for i in range(len(scores)):
        for j in range(i + 1, len(scores)):
            # Desenha o inicio da partida
            draw_match([scores[i].pair_name, scores[j].pair_name], PAIRS)
            # Aguarda
            pygame.time.wait(int(waiting))
            print(f"MATCH OF {number} GAMES BETWEEN: {scores[i].pair_name} AND {scores[j].pair_name}.")
            wins = run_match(judge, PAIRS[scores[i].pair_name], PAIRS[scores[j].pair_name], number, speed)
            print(f"RESULT: {scores[i].pair_name} HAD {wins[0]} WINS, AND {scores[j].pair_name} HAD {wins[1]} WINS.")
            # Desenha o fim da partida
            draw_match([scores[i].pair_name, scores[j].pair_name], PAIRS, start = False, lossers = [wins[0] < wins[1], wins[0] > wins[1]])
            # Aguarda
            pygame.time.wait(int(waiting))
            if wins[0] > wins[1]:
                scores[i].new_match_win(wins = wins[0], ties = number - wins[0] - wins[1], losses = wins[1])
                scores[j].new_match_losse(wins = wins[1], ties = number - wins[0] - wins[1], losses = wins[0])
            elif wins[0] < wins[1]:
                scores[i].new_match_losse(wins = wins[0], ties = number - wins[0] - wins[1], losses = wins[1])
                scores[j].new_match_win(wins = wins[1], ties = number - wins[0] - wins[1], losses = wins[0])
            else:
                scores[i].new_match_tie(wins = wins[0], ties = number - wins[0] - wins[1], losses = wins[1])
                scores[j].new_match_tie(wins = wins[1], ties = number - wins[0] - wins[1], losses = wins[0])

    # Ordena as duplas pelo placar				
    scores = sorted(scores, key=lambda x: x.sorting_attribute, reverse = True)	
    # Desenha o podium
    draw_podium(scores, PAIRS)
    print("RESULTS:")
    for i in range(len(scores)):
        key = scores[i].pair_name
        print(f"{i+1} - {key} ({PAIRS[key][0]} and {PAIRS[key][1]}")
        print("------", scores[i])
    while True:	
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()	    
