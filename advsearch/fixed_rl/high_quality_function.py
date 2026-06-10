"""

W[i] = W[i] + Alpha * (r(s + 1) - r(s))*f[i](s)
Onde:
    W é o vetor de pesos, 
        Chamarei de vetor de pesos estretanto grande parte dos valores presentes neste vetor não serão pesos e sim um valor absoluto da configuração da feature associada. Ou seja para cada W[i] existe um f[i]. Apesar disso, nada impede que os valores em W sejam vistos como pesos.
    f[i] é a flag sobre a ocorrência ou não de uma configuração específica de uma feature específica. 
    r(s) é função de avaliação aplicada ao estado 
        ou seja o somatório dos respectivos valores de cada ocorrência de configuração específica de cada feature do estado
    s é o estado atual

Evitando análise de configurações que não ocorreram:
    Uma vez que f[i] retorna a ocorrência ou não de uma configuração específica de uma feature específica, haverão diversos f[i] que retornarão 0, pois cada feature só pode estar em uma combinação. Logo para evitar operações irrelevantes usarei a seguinte algoritmo:
    erro = r(s+1) - r(s)
    update_value = alpha*erro
    for pettern_feature, indice in pattern_features:
        configuração = configuração(pettern_feature)
        w_dict[indice][configuração] = w_dict[indice][configuração] + update_value/occurrence_count(configuração)
    Onde pattern_features será uma lista duplas
    Em cada dupla de petter features o primeiro elemento é uma lista com as posições no tabuleiro referentes ao padrão e o segundo elemento é um índice associado há pettern_feature.
    A função configuração percorre as posições do tabuleiro listadas em pattern_feature crindo uma string juntando cada valor das posições, onde os valores podem ser {'B', 'W', '.'}; essa string é retornada 
    Usando o indice associado a pattern_feature e a sua configuração específica podemos encontrar o seu valor associado e atualizá-lo. 
    w_dict será um vetor de dicionários onde cada posição deste vetor guarda um dicionário com os valores associados as configurações da feature referente.

Decidindo o próximo estado:
    Como é possível notar no algoritmo é necessário um estado s + 1, ou seja, um estado sucessor do estado atual para calcular o erro.
    Este estado sucessor será escolhido usando uma política e-greedy. Onde e começará com 0.3 e o longo das partidas auto-jogadas será diminuido. Em e ocorrências será escolhido um estado sucessor totalmente aleatório, nas 1-e ocorrências será escolhido um estado sucessor baseado em uma busca MTD(f) usando a própria função de avaliação que está sendo treinada.

Ao finalizar o loop de partidas o vetor será salvo em um arquivo

Tenta abrir o arquivo de vetor de pesos, caso ele exista, para continuar o treinamento a partir do ponto onde parou. Caso contrário, inicia-se um novo vetor de pesos com valores iniciais.

15 estágios, 4 jogadas cada -> 15 vetores


Problema: 
    Descrição:
        Dado que a configuração a seja reflexão da configuração b e vice-versa, como mapear as duas configurações para a mesmma variável?
    Motivação:
        Algumas pettern feature tem reflexões, ou seja, duas configurações, a e b, são na verdade a mesma configuração uma vez que b é a configuração a refletida e vice-versa. Logo espera-se que essas configuração tenham o mesmo valor. Para terem o mesmo valor é preciso que as duas configurações mapeiem para a mesma variável. Como fazer isso? 
    Considerações:
        Atributos que falem sobre a posição de uma casa no tabuleiro devem ser descartadas, pois não podem ser utilizados na criação de um valor hash
        Em nenhuma pattern feature usada atualmente é possível aplicar rotações, isso significa que um valor estará associado a no máximo duas configurações específicas.
        No espelhamento a == reverse(b)
        A configuração de uma pattern feature será uma string
        Precisamos criar a string de forma a tornar a == reverse(b) 
    Solução parical:
        Ordenar a listas de posições associadas a feature de forma que a reversa da string a ser construída mantenha as casas de mesmo tipo nas mesmas posicões. 
        Problema da solução parcial:
            Tal solição só é aplicável para padrões em que no eixo de espelhamento haja no máximo 1 casa, pois se existir mais de uma casa de tipo exclusivo, ou seja, ser a única casa de seu tipo, não possível criar uma ordem que a reflexão mude o tipo da casa.
        Separar cada lista de posições em duas partes: A parte espelhável e parte sobre o eixo de espelhamento e consequentemente não espelhável.
        Decisão: padronizar todas as listas, gastar mais espaço e ter uma função com apenas um caso ou ter dois tipos de listas, economizar espaço, ter uma função com dois casos. Escolha ter dois tipos.

To do:
    Verificar questão de n-1 valorores possíveis
    Implementar função de avaliação:
        Carregar o vetor do arquivo pkl e usá-lo na avaliação do estado


"""

import pickle
from ..othello.gamestate import GameState
from ..othello.board import Board
import random
from ..your_agent.MTD_f_depth import Agent
from ..your_agent.othello_minimax_count import evaluate_count
import time
from datetime import datetime
from .aid_functions import *
from .pattern_features import *
import numpy as np

class Train:
    partidas = 1000000
    def __init__(self, alpha=0.1, gamma=0.95,):
        self.average_error = 0
        self.it_count = 0
        self.average_match_error = 0
        self.match_inside_count = 0
        self.alpha = alpha
        self.gamma = gamma
        self.state = None
        self.next_state = None
        self.get_vectors_list()


    def init_vectors(self) -> list:
        self.vectors_list = list()
        for i in range(15):
            vector = list()
            vector.append(0.0) ##Bias
            for j in range(46): ##Pattern_features
                vector.append(dict())
            vector.append(0.0) ##Parity_feature
            self.vectors_list.append(vector)
        return self.vectors_list

    def get_vectors_list(self) -> list:
        """Tenta pegar a lista de vetores do arquivo vectors.pkl, se não existir, cria os vetores"""
        try:
            with open("advsearch/fixed_rl/new_vectors.pkl", "rb") as file:
                self.vectors_list = pickle.load(file)
        except:
            self.vectors_list = self.init_vectors()
        return self.vectors_list
    
        
    def softmax(self, state:GameState):
        # Seleciona os top 3 movimentos com maior valor de avaliação
        # Usa uma busca para cada um dos estados sucessores dos top 3 movimentos para escolher o próximo estado
        legal_moves = state.legal_moves()
        next_states_values = []
        for move in legal_moves:
            next_state = state.next_state(move)
            value, _ = self.evaluate_state(next_state)
            next_states_values.append([next_state, value])
        for i in range(len(next_states_values)):
            next_states_values[i][1] = np.exp(next_states_values[i][1]/self.get_temp(get_stage(state)))
        total_value = sum([state[1] for state in next_states_values])
        prob = random.random()
        cumulative_prob = 0.0
        for state, value in next_states_values:
            cumulative_prob += value / total_value
            if prob < cumulative_prob:
                return state
            
    def get_temp(self, stage):
        if stage <= 10:
            return 12 - stage
        else:
            return 1
        
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

        next_state_value, next_state_occurances = self.evaluate_state(self.next_state)
        current_state_value, current_state_occurances = self.evaluate_state(self.state, vector)
        self.it_count += 1
        self.match_inside_count += 1
        erro =  (self.gamma * next_state_value) - current_state_value
        self.average_error += (abs(erro) - self.average_error)/self.it_count
        self.average_match_error += (abs(erro) - self.average_match_error)/self.match_inside_count
        if abs(erro) > self.max_error_match:
            self.max_error_match = erro
        update_value = self.alpha * erro / current_state_occurances
        # if update_value > 128 or update_value < -128:
        #     print("Update value before clipping: ", update_value)
        #     update_value = 128 if update_value > 0 else -128
        vector[0] += update_value 
        for pattern_feature, indice in pattern_features: ##Pattern_features
            configuração = get_simple_conformation(pattern_feature, self.state.board.tiles)
            self.update_simple_conformation(vector[indice], configuração, update_value)

        for pattern_feature, indice in complex_patter_features:
            configuração = get_complex_conformation(pattern_feature, self.state.board.tiles) 
            self.update_complex_conformation(vector[indice], configuração, update_value)

        for pattern_feature, indice in non_reflexible_pattern:
            configuração = get_simple_conformation(pattern_feature, self.state.board.tiles)
            if null_conformation(configuração):
                continue
            if vector[indice].get(configuração) != None:
                vector[indice][configuração]["value"] += update_value
                vector[indice][configuração]["count"] += 1
            else:
                vector[indice][configuração] = {"value": update_value, "count": 1}

        if parity_feature(self.state) == 1:
            vector[-1] += update_value ##Parity_feature

    def update_vectors_soft(self):
        stage = get_stage(self.state)
        self.update_vector()
        for i in range(1, 3):
            if stage + i <= 14:
                self.update_vector(self.vectors_list[stage + i])
            if stage - i >= 0:
                self.update_vector(self.vectors_list[stage - i])


            
    def update_simple_conformation(self, dict:dict, configuração, update_value):
        if null_conformation(configuração):
            return
        if configuração in dict:
            dict[configuração]["value"] += update_value
            dict[configuração]["count"] += 1
            return
        r_config = configuração[::-1]
        if r_config in dict:
            dict[r_config]["value"] += update_value
            dict[r_config]["count"] += 1
            return
        dict[configuração] = {"value": update_value, "count": 1}
        return
    
    def update_complex_conformation(self, dict:dict, configuração, update_value):

        config = configuração[0] + configuração[1]
        if null_conformation(config):
            return
        if config in dict:
            dict[config]["value"] += update_value
            dict[config]["count"] += 1
            return
        r_config = configuração[0][::-1] + configuração[1]
        if r_config in dict:
            dict[r_config]["value"] += update_value
            dict[r_config]["count"] += 1
            return
        dict[config] = {"value": update_value, "count": 1}
        return
            

    def evaluate_state(self, state:GameState, vector=None) -> float:
        """
        Esta é função r(s), a função de avaliação aplicada ao estado, ou seja, o somatório dos respectivos valores de cada ocorrência de configuração específica de cada feature do estado

        :param vector: será o vetor de dicionários com os valores a serem somados, ou seja, o vetor de pesos. Ele é necessário para acessar os valores associados as configurações específicas de cada feature. Se nenhum vetor em específico for passado será usado o vetor do estagio atual do estado. É possível passar um vetor que não seja o do estágio atual para que a estimativa de parâmetros seja feita de forma mais suave, ou seja, considerar que estágios próximos tenham valores próximos. Um mesmo estado será usado para atualizar os pesos dos vetores dos estágios d, d±1, d±2, onde d é o estágio atual do estado. 
        """
        if state.is_terminal():
            return evaluate_count(state, 'B'), None
        value = 0.0
        if vector is None:
            stage = get_stage(state)
            vector = self.vectors_list[stage]
        
        value += vector[0] ##Bias
        count_occurrence = 1

        for pattern_feature, indice in pattern_features: ##Pattern_features
            configuração = get_simple_conformation(pattern_feature, state.board.tiles)
            if not null_conformation(configuração):
                value += get_simple_conformation_value(configuração, vector[indice])
                count_occurrence += 1

        for pattern_feature, indice in complex_patter_features:
            configuração = get_complex_conformation(pattern_feature, state.board.tiles) 
            if not null_conformation(configuração):
                value += get_complex_conformation_value(configuração, vector[indice])
                count_occurrence += 1

        for pattern_feature, indice in non_reflexible_pattern:
            configuração = get_simple_conformation(pattern_feature, state.board.tiles)
            if null_conformation(configuração):
                continue
            returned_entry = vector[indice].get(configuração)
            if returned_entry != None:
                value += returned_entry["value"]
                count_occurrence += 1


        if parity_feature(state) == 1:
            value += vector[-1] ##Parity_feature
            count_occurrence += 1

        return (value,count_occurrence)
    


    def run_training(self):
        """
        """
        try:
            for x in range(self.partidas):
                self.state = GameState(Board(), 'B')
                print("Simulando partida ", x + 1)
                self.average_match_error = 0
                self.match_inside_count = 0
                self.max_error_match = 0
                while not self.state.is_terminal():
                    self.next_state = self.softmax(self.state)
                    self.update_vectors_soft()
                    self.state = self.next_state
                print(f"Match average erro: {self.average_match_error} Max match error: {self.max_error_match}")
                with open("advsearch/fixed_rl/new_vectors.pkl", "wb") as file:
                    pickle.dump(self.vectors_list, file, protocol=pickle.HIGHEST_PROTOCOL)
                if (x+1)%1000 == 0:
                    with open("advsearch/fixed_rl/vectors_log/Tiny_train_log.txt", "a") as tiny:
                        tiny.write(f"{x}, {self.average_error}\n")
                if (x + 1)%(100000) == 0:
                    self.alpha *= 0.75
                if (x)%(self.partidas//100) == 0:
                    
                    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                    log_path = f"advsearch/fixed_rl/vectors_log/Train_{timestamp}_{x+1}.txt"
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
                    pkl_path = f"advsearch/fixed_rl/vectors_log/vectors_{timestamp}_{x+1}.pkl"
                    with open(pkl_path, "wb") as file:
                        pickle.dump(self.vectors_list, file, protocol=pickle.HIGHEST_PROTOCOL)
        except KeyboardInterrupt:
            print("\nInterrupção detectada!")
        finally:
            print("Salvando última iteração em arquivo....")
            with open("advsearch/fixed_rl/new_vectors.pkl", "wb") as file:
                    pickle.dump(self.vectors_list, file, protocol=pickle.HIGHEST_PROTOCOL)
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_path = f"advsearch/fixed_rl/vectors_log/Train_{timestamp}_{x+1}.txt"
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
            pkl_path = f"advsearch/fixed_rl/vectors_log/vectors_{timestamp}_{x+1}.pkl"
            with open(pkl_path, "wb") as file:
                pickle.dump(self.vectors_list, file, protocol=pickle.HIGHEST_PROTOCOL)
            print("Progesso salvo com sucesso!")
                


                

                


    # def get_simple_setting_value(configuração:str, dict:dict):
    #     """
    #     Retorna o valor associado a uma configuração específica de uma pattern_feature. Também considera que o valor associado a configuração pode estar armazenado na versão espelhada da configuração, logo procura o valor na chave da configuração espelhada também. Esta é a versão simples da função, por isso assume-se que seja um espelhamento simples e procura usando a string inversa como chave

    #     :param configuração: Uma configuração específica de uma patter_feature, ou seja, a string formada pela junção dos caracteres que representam o que há em cada uma das casas do tabuleiro presentes na lista de posições da pattern_feature. Será a chave a ser acessada em dict
    #     :param dict: o dicionário dos valores da associados a cada configuração da pattern_feature
    #     """ 
    #     value = dict.get(configuração)
    #     if value != None:
    #         return value
    #     r_config = configuração[::-1]
    #     value = dict.get(r_config)
    #     if value != None:
    #         return value
    #     return 0
    
    # def get_complex_setting_value(configuração:list, dict:dict):
    #     """
    #     Retorna o valor associado a uma configuração específica de uma pattern_feature. Também considera que o valor associado a configuração pode estar armazenado na versão espelhada da configuração, logo procura o valor na chave da configuração espelhada também. Esta é a versão complexa da função, por isso assume-se que seja um espelhamento complexo onde existe mais de uma casa sobre o eixo de espelhamento, ou seja, mais de uma casa que não pode ser afetada pelo espelhamento.

    #     :param configuração: será uma lista
    #    """


        

if __name__ == "__main__":
    rl_train = Train()
    print("Running train...")
    rl_train.run_training()