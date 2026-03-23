
from typing import Tuple, Callable
import datetime
import time
from ..tttm import board as board
from datetime import datetime
import othello_minimax_count

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
    player = state.player
    time_limit = float(time.time()) + time_amount
    start_time = time.time()
    move_value, best_move = max_value(state, alpha, beta, 0, time_limit, eval_func, player)
    end_time = time.time()
    """for move in state.legal_moves():
        new_state = state.next_state(move)
        # with open(log_path, 'a') as log_file:
        #     log_file.write(f"Evaluating move: {move}\n")
        move_value = min_value(new_state, alpha, beta, 1, time_limit, eval_func)
        # with open(log_path, 'a') as log_file:
        #     log_file.write(f"Move: {move}, Value: {move_value}\n")
        if move_value > alpha:
            alpha = move_value
            best_move = move"""
    with open(log_path, 'a') as log_file:
        log_file.write(f"Player: {player} Best move will me maked: {best_move} with value: {move_value} calculed in {end_time - start_time} seconds\n\n\n\n\n\n\n\n\n\n\n\n\n\n")
    return best_move

def max_value(state, alpha, beta, depth, time_limit: float, eval_func, player, parent_state = None) -> float:
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
    if state.is_terminal():
        val_return =  othello_minimax_count.evaluate_count(state, player) 
        return val_return
    elif (time_limit != -1 and time.time() >= time_limit):
        """ with open(log_path, 'a') as log_file:
            log_file.write(f"Max avaliando estado, player: {state.player}\n") """
        val_return = (eval_func(state, player), (0, 0))
        with open(log_path, 'a') as log_file:
             for x in range(depth):
                 log_file.write("  ")  # indent for better visualization of the tree
        #     log_file.write(f"State:\n{state.board.decorated_str(colors = False)}\n\n")
             log_file.write(f"Max Evaluating depth {depth} val_return: {val_return}\n")
             
        return val_return
    
    ##Recursive case: compute the maximum value of the state for the player to move
    ##For each legal move, compute the next state and call min_value on it to get the value of the move.
    best_move = 0
    """ if state.player != player:
        with open(log_path, 'a') as log_file:
            log_file.write(f"WARNING! ")
    with open(log_path, 'a') as log_file:
        log_file.write(f"max, player: {player}, state.player: {state.player}\n") """
    legal_moves = list(state.legal_moves())
    for move in range(0, len(legal_moves)):
         new_state = state.next_state(legal_moves[move])
         # with open(log_path, 'a') as log_file:
         #     for x in range(depth):
         #         log_file.write("  ")  # indent for better visualization of the tree
         #     log_file.write(f"Max Evaluating move: {move} at depth {depth}\n")
         rest_time = time_limit - time.time()
         time_division = float(rest_time)/(len(legal_moves) - move)
         if new_state.player == player:
            move_value = max_value(new_state, alpha, beta, depth + 1, time.time() + time_division, eval_func, player, state)[0]
         else:
            move_value = min_value(new_state, alpha, beta, depth + 1, time.time() + time_division, eval_func, player, state)
            
         # with open(log_path, 'a') as log_file:
         #     for x in range(depth):
         #         log_file.write("  ")  # indent for better visualization of the tree
         #     log_file.write(f"Max Move: {move}, Value: {move_value}\n")
         if move_value > alpha:
             alpha = move_value
             best_move = move
         if alpha > beta and (parent_state == None or parent_state.player != state.player):
             # with open(log_path, 'a') as log_file:
             #     for x in range(depth):
             #         log_file.write("  ")  # indent for better visualization of the tree
             #     log_file.write(f"Max Pruning at move: {move} with value: {move_value}\n")
             return alpha, best_move
    val_return = (alpha, legal_moves[best_move])
    """  with open(log_path, 'a') as log_file:
         for x in range(depth):
             log_file.write("  ")  # indent for better visualization of the tree
         log_file.write(f"At depth {depth} best move: {best_move} val_return: {val_return}\n") """
    return val_return

def min_value(state, alpha, beta, depth, time_limit: float, eval_func, player, parent_state) -> float:
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
    if state.is_terminal():
        val_return =  othello_minimax_count.evaluate_count(state, player) 
        return val_return  
    elif (time_limit != -1 and time.time() >= time_limit):
        """ with open(log_path, 'a') as log_file:
            log_file.write(f"Min avaliando estado, player: {state.player}\n") """
        return_val = eval_func(state, player)
        with open(log_path, 'a') as log_file:
            for x in range(depth):
                log_file.write("  ")  # indent for better visualization of the tree
            #log_file.write(f"State:\n{state.board.decorated_str(colors = False)}\n\n")
            log_file.write(f"Min Evaluating depth: {depth} with utility: {return_val}\n")
        return return_val
    
    ##Recursive case: compute the minimum value of the state for the player to move 
    ##For each legal move, compute the next state and call max_value on it to get the value of the move.
    """ if state.player == player:
        with open(log_path, 'a') as log_file:
            log_file.write(f"WARNING! ")
    with open(log_path, 'a') as log_file:
        log_file.write(f"Min, player: {player}, state.player: {state.player}\n") """
    legal_moves = list(state.legal_moves())
    for move in range(len(legal_moves)):
         new_state = state.next_state(legal_moves[move])
         # with open(log_path, 'a') as log_file:
         #     for x in range(depth):
         #         log_file.write("  ")  # indent for better visualization of the tree
         #     log_file.write(f"Min Evaluating move: {move} at depth {depth}\n")
         rest_time = time_limit - time.time()
         time_division = float(rest_time)/(len(legal_moves) - move)
         if new_state.player == player:
            move_value, move_return = max_value(new_state, alpha, beta, depth + 1, time.time() + time_division, eval_func, player, state)
         else:
            move_value = min_value(new_state, alpha, beta, depth + 1, time.time() + time_division, eval_func, player, state)
         """ with open(log_path, 'a') as log_file:
              for x in range(depth):
                  log_file.write("  ")  # indent for better visualization of the tree
              log_file.write(f"Min received move_Return: {move_return}, move_value: {move_value}\n") """
         beta = min(beta, move_value)
         if beta < alpha and parent_state.player != state.player:
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
