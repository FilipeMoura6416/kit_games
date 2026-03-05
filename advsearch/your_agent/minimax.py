import random
from typing import Tuple, Callable



def minimax_move(state, max_depth:int, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game state.
    :param state: state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    raise NotImplementedError()

def max_value(state, alpha, beta, depth, max_depth, eval_func):
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
    if state.is_terminal() or (max_depth != -1 and depth >= max_depth):
        return eval_func(state, state.player)
    
    ##Recursive case: compute the maximum value of the state for the player to move
    ##For each legal move, compute the next state and call min_value on it to get the value of the move.
    for move in state.legal_moves():
         new_state = state.next_state(move)
         move_value = min_value(new_state, alpha, beta, depth + 1, max_depth, eval_func)
         alpha = max(alpha, move_value)
         if alpha >= beta:
             return alpha
    return alpha

def min_value(state, alpha, beta, depth, max_depth, eval_func):
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
    if state.is_terminal() or (max_depth != -1 and depth >= max_depth):
        return eval_func(state, state.player)
    
    ##Recursive case: compute the minimum value of the state for the player to move
    ##For each legal move, compute the next state and call max_value on it to get the value of the move.
    for move in state.legal_moves():
         new_state = state.next_state(move)
         move_value = max_value(new_state, alpha, beta, depth + 1, max_depth, eval_func)
         min_value = min(min_value, move_value)
         beta = min(beta, move_value)
         if beta <= alpha:
             return beta
    return min_value
