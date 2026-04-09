import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import log_path 
from .minimax import minimax_move
import json
from .othello_minimax_count import evaluate_count
from .minimax import log_path

EVAL_TEMPLATE = [
    [92, 15, 49, -25, -25, 49, 15, 92],
    [15, -55, -69, 66, 66, -69, -55, 15],
    [49, -69, -68, -29, -29, -68, -69, 49],
    [-25, 66, -29, 24, 24, -29, 66, -25],
    [-25, 66, -29, 24, 24, -29, 66, -25],
    [49, -69, -68, -29, -29, -68, -69, 49],
    [15, -55, -69, 66, 66, -69, -55, 15],
    [92, 15, 49, -25, -25, 49, 15, 92]
]

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.
    
    return minimax_move(state, 4.9, evaluate_mask)


def evaluate_mask(state, player:str, state_is_terminal=False) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on the positional value of the pieces.
    You must use the EVAL_TEMPLATE above to compute the positional value of the pieces.
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    """ with open("mask.json", 'r') as mask_file:
        EVAL_TEMPLATE = json.load(mask_file) """
    if state_is_terminal:
        return evaluate_count(state,player)
    count_player = 0
    for row in range(0, int(len(state.board.tiles))):
        for cell in range(0, int(len(state.board.tiles[row]))):
            if state.board.tiles[row][cell] == player:
                count_player += EVAL_TEMPLATE[row][cell]
            elif state.board.tiles[row][cell] != Board.EMPTY:
                count_player -= EVAL_TEMPLATE[row][cell]
            """ with open(log_path, 'a') as log_file:
                 log_file.write(f"cell: {state.board.tiles[row][cell]} player: {player}\n") """
    """ with open(log_path, 'a') as log_file:
                 log_file.write(f"Count_player: {count_player}\n") """
                
    return count_player

    