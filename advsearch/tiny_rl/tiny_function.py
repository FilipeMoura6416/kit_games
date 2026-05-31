import pickle
from ..othello.gamestate import GameState
from ..othello.board import Board
import random
from .tiny_mtdf import Agent
from ..your_agent.othello_minimax_count import evaluate_count
import time
from datetime import datetime
from .tiny_aid_functions import *
from .tiny_pattern_features import *

class Train:
    partidas = 1000
    def __init__(self, alpha=0.95, gamma=0.95, epsilon=0.3):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon
        self.state = None
        self.next_state = None
        self.get_vectors_list()

    def init_vectors(self) -> list:
        self.vectors_list = list()
        for i in range(1):
            vector = list()
            vector.append(random.choice(range(-10, 11))) ##Bias
            for j in range(6): ##Pattern_features
                vector.append(dict())
            self.vectors_list.append(vector)
        return self.vectors_list

    def get_vectors_list(self) -> list:
        """Tenta pegar a lista de vetores do arquivo vectors.pkl, se não existir, cria os vetores"""
        try:
            with open("advsearch/tiny_rl/vectors_log/last_vectors.pkl", "rb") as file:
                
                self.vectors_list = pickle.load(file)
        except:
            self.vectors_list = self.init_vectors()
        return self.vectors_list
    
    def e_greedy(self, state:GameState):
        legal_moves = state.legal_moves() 
        if random.random() < self.epsilon:
            return random.choice(list(legal_moves))
        else:
            ##Executa uma busca com MTD(f) usando a função de avaliação atual para escolher o próximo estado
            agent_search = Agent(state, self.vectors_list)
            return agent_search.iterative_deepening(2)

    def update_vector(self, vector=None):
        """
        erro = r(s+1) - r(s)
        update_value = alpha*erro
        for pettern_feature, indice in pattern_features:
            configuração = configuração(pettern_feature)
            w_dict[indice][configuração] = w_dict[indice][configuração] + update_value

        """
        if vector is None:
            stage = get_stage(self.state)
            vector = self.vectors_list[stage]
        erro =  self.gamma * self.evaluate_state(self.next_state, vector) - self.evaluate_state(self.state, vector)
        if self.next_state.is_terminal():
            print(f"Erro:{erro}")
        update_value = self.alpha * erro / 6
        print(f"Update value: {update_value}")
        vector[0] += update_value 
        for pattern_feature, indice in pattern_features: ##Pattern_features
            configuração = get_simple_conformation(pattern_feature, self.state.board.tiles)
            self.update_simple_conformation(vector[indice], configuração, update_value)

            
    def update_simple_conformation(self, dict:dict, configuração, update_value):
        if null_conformation(configuração):
            return
        if configuração in dict:
            # if update_value != 0:
            #     print(f"Update value: {update_value*min(1, dict[configuração]["count"]/50)/dict[configuração]["count"]}")
            dict[configuração]["value"] += update_value*min(1, dict[configuração]["count"]/50)
            dict[configuração]["count"] += 1
            return
        r_config = configuração[::-1]
        if r_config in dict:
            # if update_value != 0:
            #     print(f"Update value: {update_value*min(1, dict[r_config]["count"]/50)/dict[r_config]["count"]}")
            dict[r_config]["value"] += update_value*min(1, dict[r_config]["count"]/50)
            dict[r_config]["count"] += 1
            return
        dict[configuração] = {"value": update_value*1/50, "count": 1}
        return
    
    
    def evaluate_state(self, state:GameState, vector=None) -> float:
        
        if state.is_terminal():
            return evaluate_count(state, 'B')
        value = 0.0
        if vector is None:
            stage = get_stage(state)
            vector = self.vectors_list[stage]
        
        value += vector[0] ##Bias

        for pattern_feature, indice in pattern_features: ##Pattern_features
            configuração = get_simple_conformation(pattern_feature, state.board.tiles)
            value += get_simple_conformation_value(configuração, vector[indice])

        return value 
    
    def get_conformation_value(self, configuração:str, dict:dict):
        if null_conformation(configuração):
            return 0
        value = dict.get(configuração)
        if value != None:
            return value
        return 0 
    


    def run_training(self):
        """
        """
        ##Grava em txt
        self.write_txt()
        for x in range(self.partidas):

            self.state = GameState(Board(), 'B')
            print("Simulando partida ", x + 1)
            while not self.state.is_terminal():
                move = self.e_greedy(self.state)
                self.next_state = self.state.next_state(move)
                self.update_vector()
                self.state = self.next_state

            self.save_last_vectors()
            
            if (x+1)%(self.partidas/10) == 0 and x > 0:
                #self.epsilon *= 0.95
                #self.alpha *= 0.95
                self.write_txt()
                self.save_vectors()
                
    def write_txt(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        log_path = f"advsearch/tiny_rl/vectors_log/vectors_{timestamp}.txt"
        with open(log_path, "w") as file:
            for i, vector in enumerate(self.vectors_list):
                file.write(f"Vector:{i}\n")
                for j, entry in enumerate(vector):
                    file.write(f"\tFeature: {j}\n")
                    if type(entry) == dict:
                        for key, value in entry.items():
                            file.write(f"\t\tKey: {key}, value: {value}\n")
                    else:
                        file.write(f"\t\tValue_Entry: {entry}\n")
    def save_vectors(self):
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        pkl_path = f"advsearch/tiny_rl/vectors_log/vectors_{timestamp}.pkl"
        with open(pkl_path, "wb") as file:
            pickle.dump(self.vectors_list, file, protocol=pickle.HIGHEST_PROTOCOL)

    def save_last_vectors(self):
        with open("advsearch/tiny_rl/vectors_log/last_vectors.pkl", "wb") as file:
            pickle.dump(self.vectors_list, file, protocol=pickle.HIGHEST_PROTOCOL)
                


        

if __name__ == "__main__":
    rl_train = Train()
    print("Running train...")
    rl_train.run_training()