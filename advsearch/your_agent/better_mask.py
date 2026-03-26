import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import log_path 
from .minimax import minimax_move
import subprocess
import xml.etree.ElementTree as ET
import json






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


if __name__ == "__main__":
    EVAL_TEMPLATE = [[0 for _ in range(8)] for _ in range(8)]
    best_masks_file = "best_masks.txt"
    agents = [r"advsearch/your_agent/othello_minimax_another_mask.py" , r"advsearch/your_agent/othello_minimax_mask.py"]
    print("Criando mascara...\n")

    for j in range(1):

        for linha in range(4):
            for coluna in range(linha + 1):
                EVAL_TEMPLATE[linha][coluna] = random.choice(range(-100, 101))
                
                EVAL_TEMPLATE[7 - linha][coluna] = EVAL_TEMPLATE[linha][coluna]
                EVAL_TEMPLATE[linha][7 - coluna] = EVAL_TEMPLATE[linha][coluna]
                EVAL_TEMPLATE[7 - linha][7 - coluna] = EVAL_TEMPLATE[linha][coluna]
                if linha != coluna:
                    EVAL_TEMPLATE[coluna][linha] = EVAL_TEMPLATE[linha][coluna]
                    EVAL_TEMPLATE[coluna][7 - linha] = EVAL_TEMPLATE[linha][coluna]
                    EVAL_TEMPLATE[7 - coluna][linha] = EVAL_TEMPLATE[linha][coluna]
                    EVAL_TEMPLATE[7 - coluna][7 - linha] = EVAL_TEMPLATE[linha][coluna]

        with open("mask.json", 'w') as mask_file:
            json.dump(EVAL_TEMPLATE, mask_file)
            
        another_mask_score_count = 0
        mask_score_count = 0
        for i in range(2):
            for j in range(5):
                print("Executando partida")
                result = subprocess.run(["python", "server.py", "othello" , agents[i], agents[(i + 1)%2]])
                root = ET.parse("results.xml")
                if root == None:
                    raise "Results não encontrado"
                retorno = root.findall("player")
                if retorno == None:
                    raise "Players não encontrados"
                another_mask_score_count += int(retorno[i].get("score"))
                mask_score_count += int(retorno[(i + 1)%2].get("score")) 

        if another_mask_score_count > mask_score_count:
            with open(best_masks_file, 'a') as best:
                for lines in EVAL_TEMPLATE:
                    for colluns in lines:
                        best.write(f"{colluns} ")
                    best.write("\n")
                best.write(f"Score: another_mask: {another_mask_score_count}  mask: {mask_score_count}\n\n")