import random
from typing import Tuple

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo retorna uma jogada ilegal
    # Remova-o e coloque a sua implementacao do MCTS

    return (-1, -1)


def playout(state) -> float:
    """
    Simulates a random playout from the given state until the game ends.
    Returns the score of the player who made the move in this state.

    :param state: state to simulate
    :return: score of the player who made the move in this state
    """
    
    while not state.is_terminal():
        moves = list(state.board.legal_moves(state.player))
        move = random.choice(moves)
        state = state.next_state(move)
    
    return state.winner()
