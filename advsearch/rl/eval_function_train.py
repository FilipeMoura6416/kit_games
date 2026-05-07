from ..othello.gamestate import GameState 
from ..othello.board import Board
from ..your_agent.othello_minimax_custom import Custom_eval
from ..your_agent.othello_minimax_mask import evaluate_mask
from ..your_agent.othello_minimax_count import evaluate_count
import random
import numpy

vector_path = "C:\\Users\\lfsmo\\Superpasta\\Ufrgs\\Bolsa_Game_AI\\kit_games\\advsearch\\rl\\weight_vector.txt"

def get_features(state:GameState, player):
    value_list = list()
    custom = Custom_eval(state, player)
    value_list.append(custom.check_imutable_rocks())
    value_list.append(evaluate_mask(state, player))
    value_list.append(evaluate_count(state, player))
    if not state.is_terminal():
        value_list.append(len(state.legal_moves()))
    else:
        value_list.append(0)
    if state.player != player:
        value_list[3] *= -1
    return numpy.array(value_list)

def e_greedy(state:GameState, weight_vector):
    legal_moves = state.legal_moves() 
    if random.random()%2 == 0:
        return random.choice(legal_moves)
    else:
        max_value = float("-inf")
        best_move = None
        for move in legal_moves:
            value = numpy.dot(weight_vector, get_features(state, state.player))
            if value > max_value:
                max_value = value
                best_move = move
        return best_move
    
def truncar(val, decimais):
    multiplicador = 10 ** decimais
    return int(val * multiplicador)/multiplicador

def truncar_vetor(vector):
    for i in range(len(vector)):
        vector[i] = truncar(vector[i], 3)
    return vector 



def train(alpha, gamma):
    with open(vector_path, "r+") as file:
        linhas:list= file.readlines()
        ultima_linha = linhas.pop()
        weight_vector = numpy.array(list(map(float, ultima_linha.split())), dtype=float)
         
    print(weight_vector)

    for i in range(10):
        state = GameState(Board(), 'B')
        while not state.is_terminal():
            
            move = e_greedy(state, weight_vector)
            next_state = state.next_state(move)
            if next_state.is_terminal():
                terminal_value = evaluate_count(next_state, state.player)
            else:
                terminal_value = 0
            
            state_features = get_features(state, state.player)
            next_state_features = get_features(next_state, state.player)
            ext_state = numpy.dot(weight_vector, state_features)
            ext_next_state = numpy.dot(weight_vector, next_state_features)
            delta = terminal_value + gamma * ext_next_state - ext_state
            weight_vector = weight_vector + alpha *delta* state_features
            weight_vector = truncar_vetor(weight_vector) 
            state = next_state
    with open(vector_path, "a") as file:
        for value in weight_vector:
            file.write(f"{value} ")
        file.write("\n")

train(0.1, 0.9)