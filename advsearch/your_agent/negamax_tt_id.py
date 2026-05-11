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
        with open(log_path, 'a') as log_file:
            log_file.write(f"Start: {start%100} time_limit: {time_limit%100} \n")
        move = negamax(root_state, eval_func, alpha, beta, depth_max, time_limit, root_state.state.player, None, "MAX", tt_dict=tt_dict)
        if move[1] != None:
            best_move = move[1]
            best_move_value = move[0]
        with open(log_path, 'a') as log_file:
            log_file.write(f"End: {time.time()%100} delta_time: {time.time() - start}")
            if move[1] != None:
                log_file.write("Encerrado normalmente\n\n\n")
            else:
                log_file.write("Encerrdo a força tempo esgotado\n")

        depth_max += 1
    with open(log_path, 'a') as log_file:
        log_file.write(f"move: {best_move} move_value: {best_move_value} depth: {depth_max - 1}\n")
    return best_move

def negamax(root_state:Nodo_State, eval_func, alpha, beta, depth_max, time_limit:float, my_player, previous_state, type, depth = 0, tt_dict:dict=dict()) -> tuple:
    """
    Return the best move value and best move
    """
    ##If is terminal root_state.state
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
        ## if alpha > beta and (previous_state == none or previous_state.player != root_state.state.player)
            ## return alpha, best_move

    
    ##If is terminal root_state.state or time is up
    now = time.time()
    received_alpha = alpha
    pov_player = root_state.state.player if root_state.state.player != None else Board.opponent(previous_state.player)
    with open(log_path, 'a') as log_file:
        log_file.write("\n")
        for i in range(depth):
            log_file.write("\t")
        log_file.write(f"Chamada tipo: {type} count: {root_state.state.board.piece_count["W"] + root_state.state.board.piece_count["B"] - 4} pov_player: {pov_player} move: {root_state.move}\n")
        #log_file.write(print_with_ident(root_state.state.board.tiles, depth))
    if now >= time_limit:
        return None, None 
    tt = tt_dict.get(root_state.string_board)

    if tt != None:
        root_state.value = tt[f"{pov_player}"]
        with open(log_path, 'a') as log_file:
            for i in range(depth):
                log_file.write("\t")
            log_file.write(f"Nodo ja calculado: {tt} type: {type} value pov_player: {tt[f"{pov_player}"]} pov_player: {pov_player} Depth: {depth} \n")
        return tt[f"{pov_player}"],None
    state_is_terminal = root_state.state.is_terminal()

    if depth >= depth_max or state_is_terminal:
        state_value = eval_func(root_state.state, pov_player, state_is_terminal)
        tt_dict[root_state.string_board] = {f"{pov_player}" : state_value, f"{Board.opponent(pov_player)}": -state_value, "move": None}
        root_state.value = state_value
        with open(log_path, 'a') as log_file:
            for i in range(depth):
                log_file.write("\t") 
            log_file.write(f"Eval func returned: {state_value} Depth: {depth}\n")
        return state_value, None

    if not root_state.already:
        ramification = list(root_state.state.legal_moves())
        for move in ramification:
            new_state = root_state.state.next_state(move)
            child_node = Nodo_State(new_state, move)
            root_state.children.append(child_node)

    """ with open(log_path, 'a') as log_file:
        for i in range(depth):
                log_file.write("\t")
        log_file.write("Legal_moves: ")
        for move in root_state.state.legal_moves():
            log_file.write(f"{move} ")
        log_file.write("\n")
        for i in range(depth):
                log_file.write("\t")
        log_file.write("Childs: ")
        for child in root_state.children:
            log_file.write(f"{child.move} ")
        log_file.write("\n") """

    root_state.children.sort(key=lambda a : a.value, reverse=True)
    children_list = copy.deepcopy(root_state.children)
    count_moves = 0
    best_move = None
    best_value = float("-inf")
    for child_node in root_state.children:
            
        if child_node.state.player == root_state.state.player:
            ## move_value = Call "max"
            move_value = negamax(child_node, eval_func, alpha, beta, depth_max, time_limit,my_player, root_state.state, "MAX" if type == "MIN" else "MIN", depth + 1, tt_dict=tt_dict)[0]
        else: 
            ## move_value = Call "Min"
            move_value = negamax(child_node, eval_func, -beta, -alpha, depth_max,time_limit, my_player, root_state.state,"MIN" if type == "MAX" else "MAX", depth + 1, tt_dict=tt_dict)[0]
            if move_value != None:
                move_value = -move_value

        if time.time() >= time_limit:
            return None,None
        
        if move_value > best_value:
            best_value = move_value
            best_move = child_node.move
        if move_value > alpha:
            alpha = move_value

        if alpha > beta:
            tt_dict[root_state.string_board] = {f"{root_state.state.player}" : best_value, f"{Board.opponent(root_state.state.player)}": -best_value, "move": best_move}
            root_state.value = alpha
            root_state.already = True
            with open(log_path, 'a') as log_file:
                for i in range(depth):
                    log_file.write("\t")
                log_file.write(f"Pruning returned value: {alpha} beta: {beta} best_move: {best_move} depth: {depth} received_alpha: {received_alpha} count_moves: {count_moves} values received:")
                for child in children_list:
                    log_file.write(f" {child.value}")
                log_file.write("\n")
            return alpha, best_move
        count_moves += 1
    tt_dict[root_state.string_board] = {f"{root_state.state.player}" : best_value, f"{Board.opponent(root_state.state.player)}": -best_value, "move": best_move}
    root_state.value = alpha
    root_state.already = True
    with open(log_path, 'a') as log_file:
        for i in range(depth):
            log_file.write("\t")
        log_file.write(f"Without pruning returned value: {alpha} beta: {beta} best_move: {best_move} depth: {depth} received_alpha: {received_alpha} values:")
        for child in children_list:
            log_file.write(f" {child.value}")
        log_file.write("\n")
    return alpha, best_move

def fast_eval(move) -> float:
    value = EVAL_TEMPLATE[move[1]][move[0]]
    return value

def print_with_ident(tiles, ident) -> str:
    string = ""
    tab = ""
    for i in range(ident):
        tab += "\t"
    for lines in tiles:
        string += tab
        string += f"{lines}"
        string += "\n"
    return string