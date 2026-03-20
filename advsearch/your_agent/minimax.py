
from typing import Tuple, Callable
import datetime
import time
from ..tttm import board as board
from datetime import datetime

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = f"log_{timestamp}.txt"



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
    # with open(log_path, 'w') as log_file:
    #     log_file.write("\n\n////////////////////////////Starting minimax search with alpha-beta pruning//////////////////////////////\n\n")
    #     log_file.write(f"State:\n{state.board.decorated_str(colors = False)}\n\n")
    alpha = float('-inf')
    beta = float('inf')
    best_move = None
    time_limit = time.time() + time_amount
    for move in state.legal_moves():
        new_state = state.next_state(move)
        # with open(log_path, 'a') as log_file:
        #     log_file.write(f"Evaluating move: {move}\n")
        move_value = min_value(new_state, alpha, beta, 1, time_limit, eval_func)
        # with open(log_path, 'a') as log_file:
        #     log_file.write(f"Move: {move}, Value: {move_value}\n")
        if move_value > alpha:
            alpha = move_value
            best_move = move
    # with open(log_path, 'a') as log_file:
    #     log_file.write(f"Best move: {best_move} with value: {alpha}\n")
    return best_move

def max_value(state, alpha, beta, depth, time_limit, eval_func) -> float:
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
    if state.is_terminal() or (time_limit != -1 and time.time() >= time_limit):
        # with open(log_path, 'a') as log_file:
        #     for x in range(depth):
        #         log_file.write("  ")  # indent for better visualization of the tree
        #     log_file.write(f"State:\n{state.board.decorated_str(colors = False)}\n\n")
        #     log_file.write(f"Min Evaluating state at depth {depth} with utility: {eval_func(state, state.player)}\n")
        return eval_func(state, state.player)
    
    ##Recursive case: compute the maximum value of the state for the player to move
    ##For each legal move, compute the next state and call min_value on it to get the value of the move.
    for move in state.legal_moves():
         new_state = state.next_state(move)
         # with open(log_path, 'a') as log_file:
         #     for x in range(depth):
         #         log_file.write("  ")  # indent for better visualization of the tree
         #     log_file.write(f"Max Evaluating move: {move} at depth {depth}\n")
         move_value = min_value(new_state, alpha, beta, depth + 1, time_limit, eval_func)
         # with open(log_path, 'a') as log_file:
         #     for x in range(depth):
         #         log_file.write("  ")  # indent for better visualization of the tree
         #     log_file.write(f"Max Move: {move}, Value: {move_value}\n")
         alpha = max(alpha, move_value)
         if alpha > beta:
             # with open(log_path, 'a') as log_file:
             #     for x in range(depth):
             #         log_file.write("  ")  # indent for better visualization of the tree
             #     log_file.write(f"Max Pruning at move: {move} with value: {move_value}\n")
             return alpha
    # with open(log_path, 'a') as log_file:
    #     for x in range(depth):
    #         log_file.write("  ")  # indent for better visualization of the tree
    #     log_file.write(f"Max Returning value: {alpha} for state at depth {depth}\n")
    return alpha

def min_value(state, alpha, beta, depth, time_limit, eval_func) -> float:
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
    if state.is_terminal() or (time_limit != -1 and time.time() >= time_limit):
        # with open(log_path, 'a') as log_file:
        #     for x in range(depth):
        #         log_file.write("  ")  # indent for better visualization of the tree
        #     log_file.write(f"State:\n{state.board.decorated_str(colors = False)}\n\n")
        #     log_file.write(f"Min Evaluating state at depth {depth} with utility: {eval_func(state, state.player)}\n")
        return - eval_func(state, state.player)
    
    ##Recursive case: compute the minimum value of the state for the player to move
    ##For each legal move, compute the next state and call max_value on it to get the value of the move.
    for move in state.legal_moves():
         new_state = state.next_state(move)
         # with open(log_path, 'a') as log_file:
         #     for x in range(depth):
         #         log_file.write("  ")  # indent for better visualization of the tree
         #     log_file.write(f"Min Evaluating move: {move} at depth {depth}\n")
         move_value = max_value(new_state, alpha, beta, depth + 1, time_limit, eval_func)
         # with open(log_path, 'a') as log_file:
         #     for x in range(depth):
         #         log_file.write("  ")  # indent for better visualization of the tree
         #     log_file.write(f"Min Move: {move}, Value: {move_value}\n")
         beta = min(beta, move_value)
         if beta < alpha:
             # with open(log_path, 'a') as log_file:
             #     for x in range(depth):
             #         log_file.write("  ")  # indent for better visualization of the tree
             #     log_file.write(f"Min Pruning at move: {move} with value: {move_value}\n")
             return beta
    # with open(log_path, 'a') as log_file:
    #     for x in range(depth):
    #         log_file.write("  ")  # indent for better visualization of the tree
    #     log_file.write(f"Min Returning value: {beta} for state at depth {depth}\n")
    return beta
