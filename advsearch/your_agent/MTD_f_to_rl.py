from collections import deque
from typing import Tuple, Callable
import datetime
import time
from ..tttm import board as board
from datetime import datetime
from ..othello.board import Board
from .othello_minimax_custom import EVAL_TEMPLATE
from .othello_minimax_custom import evaluate_custom
from .othello_minimax_count import evaluate_count
from ..othello.gamestate import GameState
from ..rl.aid_functions import *
import copy
from ..rl.pattern_features import *
import pickle

def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game root_state.state
    :param root_state.state: root_state.state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    agent = Agent(state)
    return agent.iterative_deepening(3)

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
    
def neg_tiles(tiles)->list:
    neg_state = list()
    for y in range(len(tiles)):
        neg_state.append(list())
        for x in range(len(tiles[0])):
            if tiles[y][x] == 'B':
                neg_state[-1].append('W')
            elif tiles[y][x] == 'W':
                neg_state[-1].append('B')
            else:
                neg_state[-1].append('.')
    return neg_state

class Dict_entry:

    def __init__(self, minScore=float("-inf"), maxScore=float("inf")):
        self.minScore = minScore
        self.maxScore = maxScore
        self.bestMove = None

class Agent:
    def __init__(self, state, vectors_list=None):

        self.root_state = Node_State(state)
        if vectors_list == None:
            with open("advsearch/rl/vectors_log/vectors.pkl", "rb") as file:
                self.vectors_list = pickle.load(file)
        self.vectors_list = vectors_list

    def eval_func(self, state:GameState, player):
        if state.is_terminal():
            return evaluate_count(state, player)
        stage = get_stage(state)
        vector = self.vectors_list[stage]

        if player == 'W':
            tiles = neg_tiles(state.board.tiles)
        else:
            tiles = state.board.tiles


        value = vector[0] ##Bias

        for pattern_feature, indice in pattern_features: ##Pattern_features
            configuração = get_simple_conformation(pattern_feature, tiles)
            value += get_simple_conformation_value(configuração, vector[indice])

        for pattern_feature, indice in complex_patter_features:
            configuração = get_complex_conformation(pattern_feature, tiles) 
            value += get_complex_conformation_value(configuração, vector[indice])

        for pattern_feature, indice in non_reflexible_pattern:
            configuração = get_simple_conformation(pattern_feature, tiles)
            if null_conformation(configuração):
                continue
            returned_entry = vector[indice].get(configuração)
            if returned_entry != None:
                value += returned_entry["value"]


        if parity_feature(state) == 1:
            value += vector[-1] ##Parity_feature

        return value 
        

    def iterative_deepening(self, time_amout):
        self.time_limit = time.time() + time_amout
        self.depth_max = 2
        f_guess = 0
        last_move = None
        while time.time() < self.time_limit:
            self.tt_dict = dict()
            f_guess, move = self.mtdf(f_guess, self.depth_max)
            if move != None:
                last_move = move
            self.depth_max += 1
            if self.depth_max >= 60:
                return last_move
        return last_move


    def mtdf(self, f_guess, depth_max):
        upper_bound = float("inf")
        lower_bound = float("-inf")
        move = None
        while lower_bound < upper_bound and time.time() < self.time_limit:
            if f_guess == lower_bound:
                gamma = f_guess + 1
            else:
                gamma = f_guess
            f_guess, move = self.test(self.root_state, gamma - 0.5, depth_max)
            if time.time() >= self.time_limit:
                return None, None
            if f_guess < gamma:
                upper_bound = f_guess
            else:
                lower_bound = f_guess
        if move == None:
            print("Move is None, returning first legal move")
            move = self.root_state.state.legal_moves().pop()
        return f_guess, move

    def test(self, node_state:Node_State, gamma, depth_max):


        if time.time() >= self.time_limit:
            return None, None
            

        memory:Dict_entry = self.tt_dict.get(node_state.string_board)
        if memory != None:
            if memory.minScore >= gamma:
               return memory.minScore, memory.bestMove
            elif memory.maxScore < gamma:
                return memory.maxScore, memory.bestMove
        else:
            memory = Dict_entry()

        if depth_max == 0 or node_state.state.is_terminal():
            
            memory.maxScore = memory.minScore = self.eval_func(node_state.state, node_state.player)
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
        node_state.pv = node_state.children[best_move].pv.copy()
        node_state.pv.appendleft(best_move)       
        return best_score, best_move
    


