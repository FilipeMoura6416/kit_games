from collections import deque
from typing import Tuple, Callable
import datetime
import time
from ..tttm import board as board
from datetime import datetime
from ..othello.board import Board
from .othello_minimax_custom import EVAL_TEMPLATE
from .custom import evaluate_custom
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
    agent = Agent(state, evaluate_custom)
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
        self.pv = deque()
    


class Dict_entry:

    def __init__(self, minScore=float("-inf"), maxScore=float("inf")):
        self.minScore = minScore
        self.maxScore = maxScore
        self.bestMove = None

class Agent:
    def __init__(self, state, eval_func):

        self.root_state = Node_State(state)
        self.eval_func = eval_func

    def iterative_deepening(self, time_amout):
        with open(log_path, 'a') as log_file:
            log_file.write(f"Iterative Deepening - Starting iterative deepening, time amount: {time_amout}, time: {time.time()}\n")
        self.time_limit = time.time() + time_amout
        self.depth_max = 2
        f_guess = 0
        last_move = None
        last_time = 0
        while time.time() + last_time < self.time_limit:
            with open(log_path, 'a') as log_file:
                log_file.write(f"\n\nIterative Deepening - Starting new search, depth_max: {self.depth_max}, time: {time.time()}, time_limit: {self.time_limit}\n")
            self.tt_dict = dict()
            start = time.time()
            f_guess, move = self.mtdf(f_guess, self.depth_max)
            last_time = time.time() - start
            if move != None:
                last_move = move
            self.depth_max += 1
            if self.depth_max >= 60:
                return last_move
        with open(log_path, 'a') as log_file:
            log_file.write(f"\nIterative Deepening - Time Limit: {self.time_limit} returned time: {time.time()} move: {last_move}\n")
        return last_move


    def mtdf(self, f_guess, depth_max):
        upper_bound = float("inf")
        lower_bound = float("-inf")
        last_time = 0
        while lower_bound < upper_bound and time.time() + last_time < self.time_limit:
            if f_guess == lower_bound:
                gamma = f_guess + 1
            else:
                gamma = f_guess
            with open(log_path, 'a') as log_file:
                log_file.write(f"\nStarting new MTD_f search, f_guess: {f_guess}, depth_max: {depth_max}, upper_bound: {upper_bound}, lower_bound: {lower_bound}, gamma: {gamma}, time: {time.time()}\n")
            start = time.time()
            f_guess, move = self.test(self.root_state, gamma - 0.0001, depth_max)
            last_time = time.time() - start
            if time.time() >= self.time_limit:
                return None, None
            if f_guess < gamma:
                upper_bound = f_guess
            else:
                lower_bound = f_guess
            with open(log_path, 'a') as log_file:
                log_file.write(f"Finished MTD_f search, f_guess: {f_guess}, depth_max: {depth_max}, upper_bound: {upper_bound}, lower_bound: {lower_bound}, gamma: {gamma}, time: {time.time()}\n")
        return f_guess, move

    def test(self, node_state:Node_State, gamma, depth_max):


        if time.time() >= self.time_limit:
            return None, None
        with open(log_path, 'a') as log_file:
            log_file.write(self.tab_string(depth_max) + f"Testing state, move: {node_state.move}, gamma: {gamma}, depth_max: {depth_max}, player: {node_state.player}\n")
            # string_board = node_state.state.board.decorated_str(colors=False)
            # string_board = string_board.split('\n')
            # for line in string_board:
            #     log_file.write(self.tab_string(depth_max-1) + line + '\n')
            

        memory:Dict_entry = self.tt_dict.get(node_state.string_board)
        if memory != None:
            if memory.minScore >= gamma:
            #    with open(log_path, 'a') as log_file:
            #         log_file.write(self.tab_string(depth_max) + f"State previous calculated minScore >= gamma returning minScore: {memory.minScore} and move: {memory.bestMove}\n")
               return memory.minScore, memory.bestMove
            elif memory.maxScore < gamma:
                # with open(log_path, 'a') as log_file: 
                #     log_file.write(self.tab_string(depth_max) + f"State previous calculated maxScore < gamma returning maxScore: {memory.maxScore} and move: {memory.bestMove}\n")
                return memory.maxScore, memory.bestMove
        else:
            memory = Dict_entry()

        if depth_max == 0 or node_state.state.is_terminal():
            
            memory.maxScore = memory.minScore = self.eval_func(node_state.state, node_state.player)
            self.tt_dict[node_state.string_board] = memory
            # with open(log_path, 'a') as log_file:
            #     log_file.write(self.tab_string(depth_max) + f"State is terminal or depth_max == 0, returning evaluation: {memory.maxScore}\n")
            return memory.minScore, None
        
        best_move = None
        best_score = float("-inf")
        if len(node_state.legal_moves) == 0:
            node_state.legal_moves = list(node_state.state.legal_moves())
            node_state.legal_moves.sort(key=lambda x: self.fast_eval(pos=x), reverse=True)


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
            
            # with open(log_path, 'a') as log_file:
            #     log_file.write(self.tab_string(depth_max - 1) + f"Move: {move}, returned_score: {returned_score}, best_score: {best_score}, gamma: {gamma}\n")
            if returned_score > best_score:
                memory.bestMove = move
                best_score = returned_score
                best_move = move

            if best_score >= gamma:
                with open(log_path, 'a') as log_file:
                    log_file.write(self.tab_string(depth_max - 1) + f"Best score: {best_score} >= gamma: {gamma}, breaking loop and returning best_score: {best_score} and move: {best_move}\n")
                break
        if best_score < gamma:
            memory.maxScore = best_score
        else:
            memory.minScore = best_score
        self.tt_dict[node_state.string_board] = memory 
        node_state.pv = node_state.children[best_move].pv.copy()
        node_state.pv.appendleft(best_move)       
        with open(log_path, 'a') as log_file:
            log_file.write(self.tab_string(depth_max) + f"Finished testing state, returning best_score: {best_score} and move: {best_move}\n")
            log_file.write(self.tab_string(depth_max) + f"PV for this node: {list(node_state.pv)}\n")
        return best_score, best_move
    
    def tab_string(self, actual_depth_max):
        camada = self.depth_max - actual_depth_max
        string = ""
        for i in range(camada):
            string += '\t'
        return string
    def fast_eval(self, pos:tuple):
        return EVAL_TEMPLATE[pos[1]][pos[0]]