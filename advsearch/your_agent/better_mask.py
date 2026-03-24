import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import log_path 
from .minimax import minimax_move


EVAL_TEMPLATE = []



"""
Criar uma máscara aleatória desafiante
Rodar um total de 10 jogos 5 para cada agente começar:
    Rodar usando arquivo de saida
    Ler arquivo de saida a computar o ganhador 
    Se a máscara desafiante vencer guardar em arquivo


EVAL_TEMPLATE = [
    [100, -30, 6, 2, 2, 6, -30,  100],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  2,   1, 1, 3, 3, 1,   1,   2],
    [  6,   1, 1, 1, 1, 1,   1,   6],
    [-30, -50, 1, 1, 1, 1, -50, -30],
    [100, -30, 6, 2, 2, 6, -30,  100]
]

Simétricos: x,y = 7 - x, y; x, 7 - y; 7 - x, 7 - y; 
1, 0 = 6, 0; 1, 7; 6, 7 
  
"""
EVAL_TEMPLATE = [[0 for _ in range(8)] for _ in range(8)]
for linha in range(4):
     for coluna in range(linha + 1):
          EVAL_TEMPLATE[linha][coluna] = random.randrange(-100, 101, 0.5)
          EVAL_TEMPLATE[7 - linha][coluna] = EVAL_TEMPLATE[linha][coluna]
          EVAL_TEMPLATE[linha][7 - coluna] = EVAL_TEMPLATE[linha][coluna]
          EVAL_TEMPLATE[7 - linha][7 - coluna] = EVAL_TEMPLATE[linha][coluna]
          if linha != coluna:
            EVAL_TEMPLATE[coluna][linha] = EVAL_TEMPLATE[linha][coluna]
            EVAL_TEMPLATE[coluna][7 - linha] = EVAL_TEMPLATE[linha][coluna]
            EVAL_TEMPLATE[7 - coluna][linha] = EVAL_TEMPLATE[linha][coluna]
            EVAL_TEMPLATE[7 - coluna][7 - linha] = EVAL_TEMPLATE[linha][coluna]

for x in range(5):
    
