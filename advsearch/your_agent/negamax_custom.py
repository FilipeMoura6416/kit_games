from typing import Tuple
from .othello_minimax_custom import evaluate_custom
from .negamax import negamax_move

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    return negamax_move(state, 4.9, evaluate_custom)