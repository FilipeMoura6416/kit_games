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

##Minimax será uma classe
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = f"game_log\\MTD_f_{timestamp}.txt"

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game root_state.state
    :param root_state.state: root_state.state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    agent = Agent(state)
    return agent.iterative_deepening(4.9)

class Node_State:
    def __init__(self, state:GameState, move=None, parent_node=None):
        self.state = state
        self.string_board = state.board.__str__()
        self.move = move
        self.parent_node = parent_node
        self.player = state.player if state.player != None else Board.opponent(parent_node.state.player)
        self.legal_moves = list()
        self.children = dict()
    


class Dict_entry:

    def __init__(self, minScore=float("-inf"), maxScore=float("inf")):
        self.minScore = minScore
        self.maxScore = maxScore
        self.bestMove = None

class Agent:
    def __init__(self, state):

        self.root_state = Node_State(state)

    def iterative_deepening(self, time_amout):
        self.time_limit = time.time() + time_amout
        depth_max = 2
        f_guess = 0
        last_move = None
        while time.time() < self.time_limit:
            with open(log_path, 'a') as log_file:
                log_file.write(f"Starting new search, depth_max: {depth_max}, time: {time.time()}, time_limit: {self.time_limit}\n")
            self.tt_dict = dict()
            f_guess, move = self.mtdf(f_guess, depth_max)
            if move != None:
                last_move = move
            depth_max += 1
            if depth_max >= 60:
                return last_move
        with open(log_path, 'a') as log_file:
            log_file.write(f"Time Limit: {self.time_limit} returned time: {time.time()} move: {last_move}\n")
        return last_move


    def mtdf(self, f_guess, depth_max):
        upper_bound = float("inf")
        lower_bound = float("-inf")
        while lower_bound < upper_bound and time.time() < self.time_limit:
            if f_guess == lower_bound:
                gamma = f_guess + 1
            else:
                gamma = f_guess
            f_guess, move = self.test(self.root_state, gamma, depth_max)
            if time.time() >= self.time_limit:
                return None, None
            if f_guess < gamma:
                upper_bound = f_guess
            else:
                lower_bound = f_guess
        return f_guess, move

    def test(self, node_state:Node_State, gamma, depth_max):


        if time.time() >= self.time_limit:
            return None, None
        with open(log_path, 'a') as log_file:
            log_file.write(f"Testing state, gamma: {gamma}, depth_max: {depth_max}\n")

        memory:Dict_entry = self.tt_dict.get(node_state.string_board)
        if memory != None:
            if memory.minScore >= gamma:
               with open(log_path, 'a') as log_file:
                   log_file.write(f"State previous calculated minScore >= gamma")
               return memory.minScore, memory.bestMove
            elif memory.maxScore < gamma:
                return memory.maxScore, memory.bestMove
        else:
            memory = Dict_entry()

        if depth_max == 0 or node_state.state.is_terminal():
            
            memory.maxScore = memory.minScore = evaluate_custom(node_state.state, node_state.player)
            self.tt_dict[node_state.string_board] = memory
            return memory.minScore, None
        
        best_move = None
        best_score = float("-inf")
        if len(node_state.legal_moves) == 0:
            node_state.legal_moves = list(node_state.state.legal_moves())

        for move in node_state.legal_moves:

            child_state = node_state.children.get(move)

            if child_state == None:
                child_state = Node_State(node_state.state.next_state(move), move, node_state)
                node_state.children[move] = child_state

            if child_state.player == node_state.player:
                returned_score, returned_move = self.test(child_state, gamma, depth_max - 1)
            else:
                returned_score, returned_move = self.test(child_state, -gamma, depth_max - 1)
                if returned_score != None:
                    returned_score = -returned_score 

            if time.time() >= self.time_limit:
                    return None, None
            if returned_score > best_score:
                memory.bestMove = move
                best_score = returned_score
                best_move = move

            if best_score >= gamma:
                break
        if best_score < gamma:
            memory.maxScore = best_score
        else:
            memory.minScore = best_score
        self.tt_dict[node_state.string_board] = memory        
        return best_score, best_move

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