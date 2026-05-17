from typing import Tuple, Callable
import datetime
import time
from ..tttm import board as board
from datetime import datetime
from ..othello.board import Board

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = f"game_log\log_{timestamp}.txt"



def minimax_move(state, time_amount, eval_func:Callable) -> Tuple[int, int]:
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
    best_move = None
    player = state.player
    time_limit = float(time.time()) + time_amount if time_amount != -1 else time_amount
    start_time = time.time()
    move_value, best_move = max_value(state, alpha, beta, 0, time_limit, eval_func, player)
    end_time = time.time()

    with open(log_path, 'a') as log_file:
        log_file.write(f"Player: {player} Best move will me maked: {best_move} with value: {move_value} calculed in {end_time - start_time} seconds\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    
    return best_move

def max_value(state, alpha, beta, depth, time_limit: float, eval_func, player, parent_state = None, sequencia=0) -> float:
    """
    A recursive fuction to compute the maximum value of a state in the minimax algorithm with alpha-beta pruning.
    Returns the maximum value of the state for the player to move, and also updates the alpha and beta values for pruning.
    
    :param state: state to evaluate (instance of GameState)
    :param alpha: alpha value for alpha-beta pruning
    :param beta: beta value for alpha-beta pruning
    :param depth: current depth of the search
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal state or a leaf state (when search is interrupted at max_depth)
    :return: the maximum value of the state for the player to move
    """
    ##Base case: if the state is terminal or we have reached the maximum depth, return the utility of the state  
    state_is_terminal = state.is_terminal()
    if (state_is_terminal or (time_limit != -1 and time.time() >= time_limit)):
        val_return = (eval_func(state, player), (0, 0))
             
        return val_return
    
    ##Recursive case: compute the maximum value of the state for the player to move
    ##For each legal move, compute the next state and call min_value on it to get the value of the move.
    best_move = 0
    legal_moves = state.legal_moves()
    count_moves = 0
    for move in legal_moves:
        new_state = state.next_state(move)
        if time_limit != -1:
            rest_time = time_limit - time.time() 
            time_division = float(rest_time)/(len(legal_moves) - count_moves)
            child_time_limit = time.time() + time_division
        else:
            child_time_limit = time_limit
        if new_state.player == player:
            move_value = max_value(new_state, alpha, beta, depth + 1, child_time_limit, eval_func, player, state, sequencia + 1)[0]
        else:
            move_value = min_value(new_state, alpha, beta, depth + 1, child_time_limit, eval_func, player, state, sequencia)
            
        if move_value > alpha:
             alpha = move_value
             best_move = move
        if alpha > beta and (parent_state == None or parent_state.player != state.player):
            return alpha, best_move
        count_moves += 1
    val_return = (alpha, best_move)
    return val_return

def min_value(state, alpha, beta, depth, time_limit: float, eval_func, player, parent_state, sequencia=0) -> float:
    """
    A recursive fuction to compute the minimum value of a state in the minimax algorithm with alpha-beta pruning.
    Returns the minimum value of the state for the player to move, and also updates the alpha and beta values for pruning.
    
    :param state: state to evaluate (instance of GameState)
    :param alpha: alpha value for alpha-beta pruning
    :param beta: beta value for alpha-beta pruning
    :param depth: current depth of the search
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal state or a leaf state (when search is interrupted at max_depth)
    :return: the minimum value of the state for the player to move
    """


    ##Base case: if the state is terminal or we have reached the maximum depth, return the utility of the state  
    state_is_terminal = state.is_terminal()
    if (state_is_terminal or (time_limit != -1 and time.time() >= time_limit)):
        return_val = eval_func(state, player)
        return return_val
    
    ##Recursive case: compute the minimum value of the state for the player to move 
    ##For each legal move, compute the next state and call max_value on it to get the value of the move.
    legal_moves = state.legal_moves()
    count_moves = 0
    best_move = None
    for move in legal_moves:
        new_state = state.next_state(move)
        if time_limit != -1:
            rest_time = time_limit - time.time() 
            time_division = float(rest_time)/(len(legal_moves) - count_moves)
            child_time_limit = time.time() + time_division
        else:
            child_time_limit = time_limit
        if new_state.player == player:
            move_value, move_return = max_value(new_state, alpha, beta, depth + 1, child_time_limit, eval_func, player, state, sequencia)
        else:
            move_value = min_value(new_state, alpha, beta, depth + 1, child_time_limit, eval_func, player, state, sequencia - 1)
        if move_value < beta:
            beta = move_value
            best_move = move
        if beta < alpha and parent_state.player != state.player:
            return beta
        count_moves += 1
    return beta
