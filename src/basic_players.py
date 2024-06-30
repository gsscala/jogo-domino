import random

# Define a classe do jogador (Player): deve ser herdada para implementar a estratégia de jogo
class Player:
    def __init__(self, ra, name, image_path = "img/none.jpg"):
        self._name = name
        self._tiles = []
        self._position = 0
        self._image_path = image_path
        self._image = None
        self._ra = ra
        
    @property
    def name(self):
        return self._name
        
    @property
    def ra(self):
        return self._ra
    
    @property
    def image_path(self):
        return self._image_path
    
    @property
    def image(self):
        return self._image
        
    @image.setter
    def image(self, value):
        self._image = value
    
    @property
    def position(self):
        return self._position
        
    @position.setter
    def position(self, value):
        self._position = value
    
    @property
    def tiles(self):
        return self._tiles.copy()
        
    @tiles.setter
    def tiles(self, value):
        self._tiles = value.copy()
    
    def remove_tile(self, tile):
        if tile in self._tiles:
            self._tiles.remove(tile)

    def __str__(self):
        return f"{self.name}({self.ra})"

    def play(self, board_extremes, play_hist):
        # Logica do jogo a ser implementada por calsses herdeiras
        pass

# Define a classe do jogador ganancioso (GreedyPlayer): joga a maior peça possível
class GreedyPlayer(Player):

    # Implementa a função de jogar seguindo a estratégia avarenta
    def play(self, board_extremes, play_hist):
        playable_tiles = self._tiles
        if len(board_extremes) > 0:
            playable_tiles = [tile for tile in self._tiles if tile[0] in board_extremes or tile[1] in board_extremes]
        highest = -1
        tile_sum = -1
        for i in range(len(playable_tiles)):
            if playable_tiles[i][0] + playable_tiles[i][1] > tile_sum:
                tile_sum = playable_tiles[i][0] + playable_tiles[i][1]
                highest = i
        if highest >= 0:
            return 1, playable_tiles[highest]
        else:
            return 1, None

# Define a classe do jogador tolo (DummyPlayer): dentre as peças possíveis joga uma aleatória
class DummyPlayer(Player):

    # Implementa a função de jogar seguindo a estratégia tonta
    def play(self, board_extremes, play_hist):        
        playable_tiles = self._tiles
        if len(board_extremes) > 0:
            playable_tiles = [tile for tile in self._tiles if tile[0] in board_extremes or tile[1] in board_extremes]
        if playable_tiles:
            return 1, random.choice(playable_tiles)
        else:
            return 1, None

