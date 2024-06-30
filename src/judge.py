import random

class Judge:
    def __init__(self):
        self.initialize()
        
    def initialize(self):
        self._board = []
        self._start = -1
        self._players_tiles = [None] * 4
        self._players = []
        self._current = 0
        self._nones = 0
        self._play_hist = []
        self._ended = False
        
    @property
    def ended(self):
        return self._ended
        
    @property
    def start(self):
        return self._start
        
    @property
    def board(self):
        return self._board.copy()
		
    # Gera todas as peças	
    def generate(self):
        dominoes = []
        for i in range(10):
            for j in range(i, 10):
                dominoes.append((i, j))
        return dominoes
	
    # Distribui as peças aos jogadores
    def distribute_tiles(self):
        dominoes = self.generate()
        tiles = random.sample(dominoes, 40)
        for i in range(4):
            self._players_tiles[i] = tiles[i * 10: (i + 1) * 10]
            self._players[i].tiles = self._players_tiles[i].copy()
    
    # Inicia um jogo novo
    def start_game(self, players, first):
        self.initialize()
        self._players = players.copy()
        self._current = first
        self.distribute_tiles()
	
    # Adiciona uma peça jogada ao tabuleiro	
    def add_tile_to_board(self, side, tile):
        if len(self._board) == 0 or (side == 0 and self._board[0][0] in tile) or (self._board[-1][1] not in tile):
            if len(self._board) == 0 or self._board[0][0] == tile[0]:
                self._board.insert(0, (tile[1], tile[0]))	
            else:
                self._board.insert(0, (tile[0], tile[1]))
            self._start += 1
        else:
            if self._board[-1][1] == tile[0]:
                self._board.append((tile[0], tile[1]))	
            else:
                self._board.append((tile[1], tile[0]))
	
    # Faz uma jogada	
    def play(self):
        if not self.ended:
            board_extremes = tuple()
            if len(self._board) > 0:
                board_extremes = (self._board[0][0],  self._board[-1][1])
            side, tile = self._players[self._current].play(board_extremes, self._play_hist.copy())
            if tile is not None and tile in self._players_tiles[self._current] and (len(board_extremes) == 0 or tile[0] in board_extremes or tile[1] in board_extremes):
                print(f"---- {self._players[self._current].name} played: {tile}")
                self._players[self._current].remove_tile(tile)
                self._players_tiles[self._current].remove(tile)
                if len(self._players_tiles[self._current]) == 0:
                    self._ended = True
                self._play_hist.append([self._current, board_extremes, side, tile])
                self.add_tile_to_board(side, tile)
                self._nones = 0
            else:
                self._nones += 1
                if self._nones == 4:
                    self._ended = True
                self._play_hist.append([self._current, board_extremes, side, None])
            self._current = (self._current + 1) % 4
			

    # Soma as peças de um jogador
    def sum_tiles(self, pos):
        s = 0
        for tile in self._players_tiles[pos]:
            s += tile[0] + tile[1]
        return s
	
    # Indica quem ganhou
    def winner(self):
        if self.ended:
            if len(self._players_tiles[0]) == 0 or len(self._players_tiles[2]) == 0:
                return 0
            elif len(self._players_tiles[1]) == 0 or len(self._players_tiles[3]) == 0:
                return 1
            s0 = self.sum_tiles(0)
            s1 = self.sum_tiles(1)
            s2 = self.sum_tiles(2)
            s3 = self.sum_tiles(3)
            if (s0 < s1 and s0 < s3) or (s2 < s1 and s2 < s3):
                return 0
            elif (s1 < s0 and s1 < s2) or (s3 < s0 and s3 < s2):
                return 1
        return None
