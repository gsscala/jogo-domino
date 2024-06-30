import argparse
from tournament import run_tournament

parser = argparse.ArgumentParser(description="Ganhe o torneio de dominó!")

# Número de tentativas, 1000 por padrão
parser.add_argument(
    "--num-matches",
    "-n",
    type = int,
    default = 1000,
    help="Número de jogos em uma partida entre duas duplas",
)

# Velocidade do jogo, 500ms por padrão
parser.add_argument(
    "--speed",
    "-s",
    type = int,
    default = 500,
    help = "Velocidade (ms) de cada jogada",
)

# Função principal    
def main(number_of_matches, speed):
    # Começa o torneio
    run_tournament(number_of_matches, speed, 5 * speed)	

if __name__ == "__main__":
    args = parser.parse_args()
    main(args.num_matches, args.speed)
