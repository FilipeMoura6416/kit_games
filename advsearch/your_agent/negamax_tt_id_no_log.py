from typing import Tuple, Callable
import datetime
import time
from ..tttm import board as board
from datetime import datetime
from ..othello.board import Board
from .othello_minimax_custom import EVAL_TEMPLATE
from .othello_minimax_custom import evaluate_custom
from ..othello.gamestate import GameState

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = f"game_log\\negamax_new_log_{timestamp}.txt"

class Nodo_State:
    def __init__(self, state:GameState, move):
        self.state = state
        self.children = list()
        self.value = fast_eval(move) if move != None else 0
        self.string_board = state.board.__str__()
        self.already = False
        self.move = move

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game root_state.state
    :param root_state.state: root_state.state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    root_state = Nodo_State(state, None)

    return negamax_move(root_state, 4.9, evaluate_custom)

def negamax_move(root_state, time_amount, eval_func:Callable) -> Tuple[int, int]:
    """
    Returns a move computed by the minimax algorithm with alpha-beta pruning for the given game root_state.state.
    :param root_state.state: root_state.state to make the move (instance of GameState)
    :param max_depth: maximum depth of search (-1 = unlimited)
    :param eval_func: the function to evaluate a terminal or leaf root_state.state (when search is interrupted at max_depth)
                    This function should take a GameState object and a string identifying the player,
                    and should return a float value representing the utility of the root_state.state for the player.
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    with open(log_path, 'a') as log_file:
        log_file.write(f"\n\nCall ---------------------------------\n\n")
    alpha = float('-inf')
    beta = float('inf')
    
    time_limit:float = time.time() + time_amount
    depth_max = 1
    move = None
    best_move = None
    best_move_value = 0
    while time.time() < time_limit:
        start = time.time()
        tt_dict = dict()
        move = negamax(root_state, eval_func, alpha, beta, depth_max, time_limit, root_state.state.player, None, "MAX", tt_dict=tt_dict)
        if move[1] != None:
            best_move = move[1]
            best_move_value = move[0]

        depth_max += 1
    return best_move

def negamax(root_state:Nodo_State, eval_func, alpha, beta, depth_max, time_limit:float, my_player, previous_state, type, depth = 0, tt_dict:dict=dict()) -> tuple:
  
    now = time.time()
    pov_player = root_state.state.player if root_state.state.player != None else Board.opponent(previous_state.player)
    if now >= time_limit:
        return None, None 
    tt = tt_dict.get(root_state.string_board)

    if tt != None:
        root_state.value = tt[f"{pov_player}"]
        return tt[f"{pov_player}"],None
    state_is_terminal = root_state.state.is_terminal()
    if depth >= depth_max or state_is_terminal:
        state_value = eval_func(root_state.state, pov_player, state_is_terminal)
        tt_dict[root_state.string_board] = {f"{pov_player}" : state_value, f"{Board.opponent(pov_player)}": -state_value, "move": None}
        root_state.value = state_value
        return state_value, None

    if not root_state.already:
        ramification = list(root_state.state.legal_moves())
        for move in ramification:
            new_state = root_state.state.next_state(move)
            child_node = Nodo_State(new_state, move)
            root_state.children.append(child_node)

    root_state.children.sort(key=lambda a : a.value, reverse=True)
    count_moves = 0
    best_move = None
    for child_node in root_state.children:
            
        if child_node.state.player == root_state.state.player:
            ## move_value = Call "max"
            move_value = negamax(child_node, eval_func, alpha, beta, depth_max, time_limit,my_player, root_state.state, "MAX" if type == "MIN" else "MIN", depth + 1, tt_dict=tt_dict)[0]
        else: 
            ## move_value = Call "Min"
            move_value = negamax(child_node, eval_func, -beta, -alpha, depth_max,time_limit, my_player, root_state.state,"MIN" if type == "MAX" else "MAX", depth + 1, tt_dict=tt_dict)[0]
            if move_value != None:
                move_value = - move_value

        if time.time() >= time_limit:
            return None,None
        
        if move_value > alpha:
            alpha = move_value
            best_move = child_node.move

        if alpha > beta and (previous_state.player != root_state.state.player):
            tt_dict[root_state.string_board] = {f"{root_state.state.player}" : alpha, f"{Board.opponent(root_state.state.player)}": -alpha, "move": best_move}
            root_state.value = alpha
            root_state.already = True
            return alpha, best_move
        count_moves += 1
    tt_dict[root_state.string_board] = {f"{root_state.state.player}" : alpha, f"{Board.opponent(root_state.state.player)}": -alpha, "move": best_move}
    root_state.value = alpha
    root_state.already = True
    return alpha, best_move

def fast_eval(move) -> float:
    value = EVAL_TEMPLATE[move[1]][move[0]]
    return value