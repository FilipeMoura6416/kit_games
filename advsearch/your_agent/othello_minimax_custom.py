import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move
from .othello_minimax_count import evaluate_count
from .minimax import log_path

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

EVAL_TEMPLATE = [
    [100, -40, 10, 8, 8, 10, -40,  100],
    [-40, -50, 1, 1, 1, 1, -50, -40],
    [ 10,   1, 2, 1, 1, 2,   1,   10],
    [  8,   1, 1, 2, 2, 1,   1,   8],
    [  8,   1, 1, 2, 2, 1,   1,   8],
    [ 10,   1, 2, 1, 1, 2,   1,   10],
    [-40, -50, 1, 1, 1, 1, -50, -40],
    [100, -40, 10, 8, 8, 10, -40,  100]
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

    return minimax_move(state, 4.9, evaluate_custom)


def evaluate_custom(state, player:str, sequencia=0, state_is_terminal=False) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    If the state is terminal, returns its utility. 
    If non-terminal, returns an estimate of its value based on your custom heuristic
    :param state: state to evaluate (instance of GameState)
    :param player: player to evaluate the state for (B or W)
    """
    if not state_is_terminal:
        moves = len(state.legal_moves())
        if state.player != player:
            moves = -moves
        
        player_value = 0
        count_pieces = 0
        for row in range(0, int(len(state.board.tiles))):
            for cell in range(0, int(len(state.board.tiles[row]))):
                if state.board.tiles[row][cell] == player:
                    player_value += EVAL_TEMPLATE[row][cell]
                    count_pieces += 1
                elif state.board.tiles[row][cell] != Board.EMPTY:
                    player_value -= EVAL_TEMPLATE[row][cell]
                    count_pieces -= 1
        adversario = 'W' if player == 'B' else 'B'
        ##Testa primeira linha
        linha_completa = 1
        for j in range(2, 7):
            if not (state.board.tiles[0][j] == state.board.tiles[0][j - 1] and state.board.tiles[0][j] != Board.EMPTY):
                linha_completa = 0
                break  
        if linha_completa:
            if state.board.tiles[0][1] == player and ((state.board.tiles[0][0] != adversario) ^ (state.board.tiles[0][7] != adversario)):
                player_value += 60
            else:
                player_value -= 60
        ##Testa ultima linha
        linha_completa = 1
        for j in range(2, 7):
            if not (state.board.tiles[7][j] == state.board.tiles[7][j - 1] and state.board.tiles[7][j] != Board.EMPTY):
                linha_completa = 0
                break  
        if linha_completa:
            if state.board.tiles[7][1] == player and ((state.board.tiles[7][0] != adversario) ^ (state.board.tiles[7][7] != adversario)):
                player_value += 60
            else:
                player_value -= 60
        ##Testa primeira coluna
        linha_completa = 1
        for j in range(2, 7):
            if not (state.board.tiles[j][0] == state.board.tiles[j-1][0] and state.board.tiles[j][0] != Board.EMPTY):
                linha_completa = 0
                break  
        if linha_completa:
            if state.board.tiles[1][0] == player and ((state.board.tiles[0][0] != adversario) ^ (state.board.tiles[7][0] != adversario)):
                player_value += 60
            else:
                player_value -= 60
         ##Testa ultima coluna
        linha_completa = 1
        for j in range(2, 7):
            if not (state.board.tiles[j][7] == state.board.tiles[j-1][7] and state.board.tiles[j][7] != Board.EMPTY):
                linha_completa = 0
                break  
        if linha_completa:
            if state.board.tiles[1][7] == player and ((state.board.tiles[0][7] != adversario) ^ (state.board.tiles[7][7] != adversario)):
                player_value += 60
            else:
                player_value -= 60


        return player_value
    else:
        return evaluate_count(state, player)


