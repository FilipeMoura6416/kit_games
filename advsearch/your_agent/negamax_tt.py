from typing import Tuple, Callable
import datetime
import time
from ..tttm import board as board
from datetime import datetime
from ..othello.board import Board
from .othello_minimax_custom import EVAL_TEMPLATE
from .othello_minimax_custom import evaluate_custom
from ..othello.gamestate import GameState


"""
In this code a fix the little error in fast_eval, move is (column, line) but i was using like (line, column) 
I keep the two codes to verify if the fixed version is better
"""
def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    return negamax_move(state, 4.8, evaluate_custom)

def negamax_move(state, time_amount, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    alpha = float('-inf')
    beta = float('inf')
    tt_dict = dict()

    return negamax(state, time.time() + time_amount, eval_func, alpha, beta, state.player, None, tt_dict=tt_dict)[1]

def negamax(state:GameState, time_limit, eval_func, alpha, beta, my_player, previous_state, depth = 0, tt_dict:dict=dict()) -> tuple:
    """
    Return the best move value and best move
    """
    ##If is terminal state
        ##Check winner
    ##If time is up 
        ##Eval
    
    ## Get legal_moves
    ## Sort
    ## For move in legal_moves
        ## Get new_state
        ## If new_state.player == my player
            ## move_value = Call "max"
        ##Else
            ## move_value = Call "Min"
        ## if move_value > alpha
            ## alpha = move_value
            ## best_move = move
        ## if alpha > beta and (previous_state == none or previous_state.player != state.player)
            ## return alpha, best_move

    
    ##If is terminal state or time is up 
    tt = tt_dict.get(state.board.__str__())
    
    pov_player = state.player if state.player != None else Board.opponent(previous_state.player)
    if tt != None and tt[f"{pov_player}"] != None:
        return tt[f"{pov_player}"]
    state_is_terminal = state.is_terminal()
    if state_is_terminal or time.time() >= time_limit:
        ##Eval            
        state_value = eval_func(state, pov_player, state_is_terminal)
        tt_dict[state.board.__str__()] = {f"{pov_player}" : state_value, f"{Board.opponent(pov_player)}": -state_value, "move": None}
        return state_value, None

    legal_moves = list(state.legal_moves())
    legal_moves.sort(key=fast_eval, reverse=True)
    count_moves = 0
    best_move = None
    for move in legal_moves:

        new_state = state.next_state(move)
        rest_time = time_limit - time.time()
        time_division = rest_time/(len(legal_moves) - count_moves)

        if new_state.player == state.player:
            ## move_value = Call "max"
            move_value = negamax(new_state, time_division + time.time(), eval_func, alpha, beta, my_player, state, depth + 1, tt_dict=tt_dict)[0]
        else: 
            ## move_value = Call "Min"
            move_value = -negamax(new_state, time_division + time.time(), eval_func, -beta, -alpha, my_player, state, depth + 1, tt_dict=tt_dict)[0]

        if move_value > alpha:
            alpha = move_value
            best_move = move

        if alpha > beta and (previous_state == None or previous_state.player != state.player):
            tt_dict[state.board.__str__()] = {f"{state.player}" : alpha, f"{Board.opponent(state.player)}": -alpha, "move": best_move}
            return alpha, best_move
        count_moves += 1
    tt_dict[state.board.__str__()] = {f"{state.player}" : alpha, f"{Board.opponent(state.player)}": -alpha, "move": best_move}
    return alpha, best_move

def fast_eval(move) -> float:
    value = EVAL_TEMPLATE[move[1]][move[0]]
    return value