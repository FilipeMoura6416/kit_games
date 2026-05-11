from typing import Tuple, Callable
import datetime
import time
from ..tttm import board as board
from datetime import datetime
from ..othello.board import Board
from .othello_minimax_custom import EVAL_TEMPLATE
from .othello_minimax_custom import evaluate_custom
from ..othello.gamestate import GameState
import copy

##Minimax será uma classe

class Nodo_State:
    def __init__(self, state:GameState, move):
        self.state = state
        self.children = list()
        self.value = fast_eval(move) if move != None else 0
        self.string_board = state.board.__str__()
        self.already = False
        self.move = move

def fast_eval(move) -> float:
    value = EVAL_TEMPLATE[move[1]][move[0]]
    return value