import pygame

# Dimensões da tela
WIDTH, HEIGHT = 1200, 800
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Domino")

# Cores
WHITE = (255, 255, 255)
BLUE_IC = (11, 149, 222) # Cor azul do IC
ORANGE_IC = (255, 115, 1) # Cor laranja do IC

# Constantes
TILE_SIZE = 36
GAP = 4
DOT_SIZE = 3
DOT_PADDING = (TILE_SIZE - 3 * DOT_SIZE) // 4 
BOARD_RIGHT = 1100
BOARD_LEFT = 100

# Posições dos potnos para cada valor da peça
START = DOT_PADDING
MIDDLE = (TILE_SIZE) // 2
END = TILE_SIZE - DOT_PADDING	
DOTS_POSITIONS = {
    0: [],
	1: [(MIDDLE, MIDDLE)],
	2: [(START, START), (END, END)],
	3: [(START, START), (MIDDLE, MIDDLE), (END, END)],
	4: [(START, START), (START, END), (END, START), (END, END)],
	5: [(START, START), (START, END), (MIDDLE, MIDDLE), (END, START), (END, END)],
	6: [(START, START), (START, END), (MIDDLE, START), (MIDDLE, END), (END, START), (END, END)],
	7: [(START, START), (START, END), (MIDDLE, START), (MIDDLE, MIDDLE), (MIDDLE, END), (END, START), (END, END)],
	8: [(START, START), (START, MIDDLE), (START, END), (MIDDLE, START), (MIDDLE, END), (END, START), (END, MIDDLE), (END, END)],
	9: [(START, START), (START, MIDDLE), (START, END), (MIDDLE, START), (MIDDLE, MIDDLE), (MIDDLE, END), (END, START), (END, MIDDLE), (END, END)]
}

		
# Desenha metade da peça de domino
def draw_half_tile(x, y, dots, horizontal = True):
    # Desenha o fondo branco
    pygame.draw.rect(SCREEN, WHITE, (x, y, TILE_SIZE, TILE_SIZE))    
    # Desenha os pontos
    for pos in DOTS_POSITIONS[dots]:
        if horizontal:
            pygame.draw.circle(SCREEN, ORANGE_IC, (x + pos[0], y + pos[1]), DOT_SIZE)
        else:
            pygame.draw.circle(SCREEN, ORANGE_IC, (x + pos[1], y + pos[0]), DOT_SIZE)
		
# Desenh uma peça de domino
def draw_domino(x, y, domino, direction = 1, horizontal = True):
    first = 0
    second = 1
    if direction < 0:
        first = 1
        second = 0
    # Desenha a primeira metade
    draw_half_tile(x, y, domino[first], horizontal)   
    # Desenha a segunda metade
    if horizontal:
        draw_half_tile(x + TILE_SIZE, y, domino[second], horizontal)
        pygame.draw.line(SCREEN, ORANGE_IC, (x + TILE_SIZE, y), (x + TILE_SIZE, y + TILE_SIZE), 2) # Linha que separa as duas metades
    else:
        draw_half_tile(x, y + TILE_SIZE, domino[second], horizontal)
        pygame.draw.line(SCREEN, ORANGE_IC, (x, y + TILE_SIZE), (x + TILE_SIZE, y + TILE_SIZE), 2) # Linha que separa as duas metades

# Desenha todas as peças colocadas numa metade do tabuleiro
def draw_half_board(board_tiles, start, end, step = 1):
    x = WIDTH // 2 - TILE_SIZE
    y = HEIGHT // 2 - TILE_SIZE // 2
    direction = step
    if step < 0:
        x += direction * (2 * TILE_SIZE + GAP)    
    for i in range(start, end, step):
        if x + 2 * direction * TILE_SIZE > BOARD_RIGHT:  # Se chegou no final direito, precisa colcar uma peça vertical
            x -= GAP
            if step < 0:
                draw_domino(x - TILE_SIZE, y + step * (2 * TILE_SIZE + GAP), board_tiles[i], horizontal = False)
            else:
                draw_domino(x - TILE_SIZE, y + step * (TILE_SIZE + GAP), board_tiles[i], horizontal = False)
            y += step * (2 * TILE_SIZE + GAP)
            x -= 3 * TILE_SIZE + GAP
            direction *= -1
        elif x < BOARD_LEFT:  # Se chegou no final esquerdo, precisa colocar uma peça vertical
            x -= direction * (2 * TILE_SIZE + GAP)
            if step < 0:
                draw_domino(x, y + step * (2 * TILE_SIZE + GAP), board_tiles[i], horizontal = False)
            else:
                draw_domino(x, y + step * (TILE_SIZE + GAP), board_tiles[i], horizontal = False)
            y += step * (2 * TILE_SIZE + GAP)
            x += TILE_SIZE + GAP
            direction *= -1
        else: # O desenho padrão é das peças horizontais
            draw_domino(x, y, board_tiles[i], direction * step)
            x += direction * (2 * TILE_SIZE + GAP)

# Desenha todas as peças colocadas no tabuleiro
def draw_board(start, board_tiles):
    SCREEN.fill(BLUE_IC)
    if start >= 0:
        draw_half_board(board_tiles, start, len(board_tiles))
        draw_half_board(board_tiles, start - 1, 0, -1)

# Posições e movimentação dos jogadores pelo número
PLAYER_POS = {
    0: (((WIDTH - 10 * (TILE_SIZE + GAP)) // 2, 2 * GAP),(1, 0), False),
    1: ((2 * GAP, (HEIGHT - 10 * (TILE_SIZE + GAP)) // 2),(0, 1), True),
    2: (((WIDTH - 10 * (TILE_SIZE + GAP)) // 2, HEIGHT - 2 * (TILE_SIZE + GAP)),(1, 0), False),
    3: ((WIDTH - 2 * (TILE_SIZE + GAP), (HEIGHT - 10 * (TILE_SIZE + GAP)) // 2),(0, 1), True)
}

# Superfície para imagens quadradas
square_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
pygame.draw.rect(square_surface, (255, 255, 255, 128), (0, 0, 100, 100))

# Desenha um jogador
def draw_player(number, image, tiles):
    x = PLAYER_POS[number][0][0]
    y = PLAYER_POS[number][0][1]
    dx = PLAYER_POS[number][1][0]
    dy = PLAYER_POS[number][1][1]
    square_surface.blit(image, (0, 0)) # Ajusta a posição da imagem no quadrado
    SCREEN.blit(square_surface, (x - dx * 3 * TILE_SIZE - (1 - dx) * 3 * GAP, y - dy * 3 * TILE_SIZE - (1 - dy) * 3 * GAP))
    for tile in tiles:
        draw_domino(x, y, tile, horizontal = PLAYER_POS[number][2])
        x += dx * (TILE_SIZE + GAP)
        y += dy * (TILE_SIZE + GAP)

# Desenha todos os jogadores
def draw_players(players):
    for player in players:
        draw_player(player.position, player.image, player.tiles)

# Desenha o jogo		
def draw_game(start, board, players):
    draw_board(start, board)
    draw_players(players)
    pygame.display.flip()
	
# Desenha uma dupla		
def draw_match_pair(pair_name, pair, x, losse = False):
    font = pygame.font.Font(None, 75)
    text_surface = font.render(pair_name, True, WHITE)
    vs_rect = text_surface.get_rect(center=(x, HEIGHT // 2 - 2 * TILE_SIZE))
    SCREEN.blit(text_surface, vs_rect)
    square_surface.blit(pair[0].image, (0, 0)) # Ajusta a posição da imagem no quadrado
    SCREEN.blit(square_surface, (x - 3 * TILE_SIZE, HEIGHT // 2))
    square_surface.blit(pair[1].image, (0, 0)) # Ajusta a posição da imagem no quadrado
    SCREEN.blit(square_surface, (x, HEIGHT // 2))
    if losse:
        # Desenha um "X" acima dos perdedores
        font = pygame.font.Font(None, 400)
        text_surface = font.render("X", True, ORANGE_IC)
        vs_rect = text_surface.get_rect(center=(x, HEIGHT // 2))
        SCREEN.blit(text_surface, vs_rect)
	
	
# Desenha o início/fim do confronto entre duas duplas		
def draw_match(pair_names, pairs, start = True, lossers = []):
    SCREEN.fill(BLUE_IC)
    # Desenha a linha branca que separa as duplas simulando um raio
    start_pos = (WIDTH // 2, HEIGHT // 4)  
    end_pos = (WIDTH // 2, 3 * HEIGHT // 4)  
    bolt_points = [(WIDTH // 2, HEIGHT // 4),
        (WIDTH // 2 + 30, HEIGHT // 3),
        (WIDTH // 2 - 20, HEIGHT // 2),
        (WIDTH // 2 + 20, 2 * HEIGHT // 3),
        (WIDTH // 2 - 10, 3 * HEIGHT // 4),
        (WIDTH // 2, HEIGHT * 3 // 4 + 30)]
    pygame.draw.lines(SCREEN, WHITE, False, bolt_points, 10) 
    # Desenha o texto "VS"
    font = pygame.font.Font(None, 200)
    text_surface = font.render("VS", True, ORANGE_IC)
    vs_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    SCREEN.blit(text_surface, vs_rect)
	#Desenha as duplas
    font = pygame.font.Font(None, 100)
    if start:
        text_surface = font.render("Início", True, WHITE)
        draw_match_pair(pair_names[0], pairs[pair_names[0]], WIDTH // 4)
        draw_match_pair(pair_names[1], pairs[pair_names[1]], 3 * WIDTH // 4)	
    else:
        text_surface = font.render("Fim", True, WHITE)
        draw_match_pair(pair_names[0], pairs[pair_names[0]], WIDTH // 4, lossers[0])
        draw_match_pair(pair_names[1], pairs[pair_names[1]], 3 * WIDTH // 4, lossers[1])
    vs_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 8))
    SCREEN.blit(text_surface, vs_rect)
    pygame.display.flip()

# Desenha o nome e as imagens da dupla	
def draw_double(name, pair, podium_rect):
    # Desenha o nome
    font = pygame.font.Font(None, 42)
    text_surface = font.render(name, True, WHITE)
    text_rect = text_surface.get_rect(center=(podium_rect.centerx, podium_rect.centery))
    SCREEN.blit(text_surface, text_rect)
    # Desenha as imagens
    SCREEN.blit(pair[0].image, (podium_rect.left - 110, podium_rect.centery - 50))
    SCREEN.blit(pair[1].image, (podium_rect.right + 10, podium_rect.centery - 50))	
	
# Desenha o podium
def draw_podium(scores, pairs):
    SCREEN.fill(BLUE_IC)
    # Define os níveis
    first_place = pygame.Rect(WIDTH // 4, HEIGHT // 4, WIDTH // 2, HEIGHT // 6)
    second_place = pygame.Rect(WIDTH // 4 + 50, HEIGHT // 4 + HEIGHT // 6 + 50, WIDTH // 2 - 100, HEIGHT // 6)
    third_place = pygame.Rect(WIDTH // 4 + 100, HEIGHT // 4 + HEIGHT // 6 + HEIGHT // 6 + 100, WIDTH // 2 - 200, HEIGHT // 6)
    # Desenha os retângulos do podium
    pygame.draw.rect(SCREEN, (255, 215, 0), first_place) #Ouro
    pygame.draw.rect(SCREEN, (192, 192, 192), second_place) #Prata
    pygame.draw.rect(SCREEN, (205, 127, 50), third_place) #Bronze
    # Desenha os nomes e as imagens das duplas ganhadoras
    if len(scores) > 0:
        draw_double("1ro - " + scores[0].pair_name, pairs[scores[0].pair_name], first_place)
    if len(scores) > 1:
        draw_double("2do - " + scores[1].pair_name, pairs[scores[1].pair_name], second_place)
    if len(scores) > 2:
        draw_double("3ro - " + scores[2].pair_name, pairs[scores[2].pair_name], third_place)
    pygame.display.flip()
	
	
