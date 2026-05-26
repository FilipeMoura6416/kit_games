"""

W[i] = W[i] + b * (r(s + 1) - r(s))*f[i](s)
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
    update_value = b*erro
    for pettern_feature, indice in pattern_features:
        configuração = configuração(pettern_feature)
        w_dict[indice][configuração] = w_dict[indice][configuração] + update_value
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
from ..your_agent.MTD_f_to_rl import Agent
from ..your_agent.othello_minimax_count import evaluate_count
import time
import datetime



pattern_features = [
    ## ==================== DIAG4 ====================
    ([(3,0), (2,1), (1,2), (0,3)], 1),   ## Diagonal 4_1
    ([(0,4), (1,5), (2,6), (3,7)], 2),   ## Diagonal 4_2
    ([(7,4), (6,5), (5,6), (4,7)], 3),   ## Diagonal 4_3
    ([(4,0), (5,1), (6,2), (7,3)], 4),   ## Diagonal 4_4

    ## ==================== DIAG5 ====================
    ([(4,0), (3,1), (2,2), (1,3), (0,4)], 5),   ## Subindo - Canto Superior
    ([(0,3), (1,4), (2,5), (3,6), (4,7)], 6),   ## Descendo - Canto Direito
    ([(7,3), (6,4), (5,5), (4,6), (3,7)], 7),   ## Subindo - Canto Inferior
    ([(3,0), (4,1), (5,2), (6,3), (7,4)], 8),   ## Descendo - Canto Esquerdo

    ## ==================== DIAG6 ====================
    ([(5,0), (4,1), (3,2), (2,3), (1,4), (0,5)], 9),
    ([(0,2), (1,3), (2,4), (3,5), (4,6), (5,7)], 10),
    ([(7,2), (6,3), (5,4), (4,5), (3,6), (2,7)], 11),
    ([(2,0), (3,1), (4,2), (5,3), (6,4), (7,5)], 12),

    ## ==================== DIAG7 ====================
    ([(6,0), (5,1), (4,2), (3,3), (2,4), (1,5), (0,6)], 13),
    ([(0,1), (1,2), (2,3), (3,4), (4,5), (5,6), (6,7)], 14),
    ([(7,1), (6,2), (5,3), (4,4), (3,5), (2,6), (1,7)], 15),
    ([(1,0), (2,1), (3,2), (4,3), (5,4), (6,5), (7,6)], 16),

    ## ==================== DIAG8 ====================
    # Apenas as duas grandes diagonais principais do tabuleiro:
    ([(7,0), (6,1), (5,2), (4,3), (3,4), (2,5), (1,6), (0,7)], 17), ## Diagonal secundária
    ([(0,0), (1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7)], 18), ## Diagonal principal

    ## ==================== HOR. / VERT. 2 ====================
    ([(1,0), (1,1), (1,2), (1,3), (1,4), (1,5), (1,6), (1,7)], 19), ## Horizontal linha 1
    ([(6,0), (6,1), (6,2), (6,3), (6,4), (6,5), (6,6), (6,7)], 20), ## Horizontal linha 6
    ([(0,1), (1,1), (2,1), (3,1), (4,1), (5,1), (6,1), (7,1)], 21), ## Vertical coluna 1
    ([(0,6), (1,6), (2,6), (3,6), (4,6), (5,6), (6,6), (7,6)], 22), ## Vertical coluna 6

    ## ==================== HOR. / VERT. 3 ====================
    ([(2,0), (2,1), (2,2), (2,3), (2,4), (2,5), (2,6), (2,7)], 23), ## Horizontal linha 2
    ([(5,0), (5,1), (5,2), (5,3), (5,4), (5,5), (5,6), (5,7)], 24), ## Horizontal linha 5
    ([(0,2), (1,2), (2,2), (3,2), (4,2), (5,2), (6,2), (7,2)], 25), ## Vertical coluna 2
    ([(0,5), (1,5), (2,5), (3,5), (4,5), (5,5), (6,5), (7,5)], 26), ## Vertical coluna 5

    ## ==================== HOR. / VERT. 4 ====================
    ([(3,0), (3,1), (3,2), (3,3), (3,4), (3,5), (3,6), (3,7)], 27), ## Horizontal linha 3
    ([(4,0), (4,1), (4,2), (4,3), (4,4), (4,5), (4,6), (4,7)], 28), ## Horizontal linha 4
    ([(0,3), (1,3), (2,3), (3,3), (4,3), (5,3), (6,3), (7,3)], 29), ## Vertical coluna 3
    ([(0,4), (1,4), (2,4), (3,4), (4,4), (5,4), (6,4), (7,4)], 30), ## Vertical coluna 4

    ## ==================== EDGE + 2X ====================
    ([(1,1), (0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (1,6)], 31), ## Borda Superior
    ([(6,1), (7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (6,6)], 32), ## Borda Inferior
    ([(1,1), (0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (6,1)], 33), ## Borda Esquerda
    ([(1,6), (0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (6,6)], 34), ## Borda Direita


    ]

complex_patter_features = [

    ## ==================== 3x3 - CORNER ====================
    (([(0,2), (0,1), (1,2), (2,1), (1,0), (2,0)], [(0,0), (1,1), (2,2)]), 43), ## Sup. Esquerdo
    (([(0,5), (0,6), (1,5), (2,6), (1,7), (2,7)], [(0,7), (1,6), (2,5)]), 44), ## Sup. Direito
    (([(7,2), (7,1), (6,2), (5,1), (6,0), (5,0)], [(7,0), (6,1), (5,2)]), 45), ## Inf. Esquerdo
    (([(7,5), (7,6), (6,5), (5,6), (6,7), (5,7)], [(7,7), (6,6), (5,5)]), 46)  ## Inf direito

]

non_reflexible_pattern = [
    ## ==================== 2x5 - CORNER ====================
    # Cantos Horizontais:
    ([(0,0), (0,1), (0,2), (0,3), (0,4), (1,0), (1,1), (1,2), (1,3), (1,4)], 35), ## Sup. Esquerdo
    ([(0,3), (0,4), (0,5), (0,6), (0,7), (1,3), (1,4), (1,5), (1,6), (1,7)], 36), ## Sup. Direito
    ([(6,0), (6,1), (6,2), (6,3), (6,4), (7,0), (7,1), (7,2), (7,3), (7,4)], 37), ## Inf. Esquerdo
    ([(6,3), (6,4), (6,5), (6,6), (6,7), (7,3), (7,4), (7,5), (7,6), (7,7)], 38), ## Inf. Direito
    # Cantos Verticais:
    ([(0,0), (1,0), (2,0), (3,0), (4,0), (0,1), (1,1), (2,1), (3,1), (4,1)], 39),
    ([(3,0), (4,0), (5,0), (6,0), (7,0), (3,1), (4,1), (5,1), (6,1), (7,1)], 40),
    ([(0,6), (1,6), (2,6), (3,6), (4,6), (0,7), (1,7), (2,7), (3,7), (4,7)], 41),
    ([(3,6), (4,6), (5,6), (6,6), (7,6), (3,7), (4,7), (5,7), (6,7), (7,7)], 42),

]

def get_simple_conformation(positions:list, tiles:list):
    """
    Retorna a configuração atual de um conjunto de posições

    :param positions: uma lista de posições do tabuleiro.

    :param tiles: tabuleiro
    """
    conformation = ""
    for pos in positions:
        x, y = pos
        conformation += tiles[x][y]
    return conformation
    
    
def get_complex_conformation(positions:tuple, tiles):
    """
    Retorna a configuração atual de um conjunto de posições

    :param positions: dupla com duas listas de posições, a primeira lista é a lista de posições reflexíveis e a segunda lista é a lista de posições não reflexíveis.
    :param tiles: tabuleiro
    """
    first, tail = positions
    conformation = get_simple_conformation(first, tiles)
    tail_conformation = get_simple_conformation(tail, tiles)
    return conformation, tail_conformation

def get_tiles(pos_list:list, tiles:list):
    """
    Junta e retorna os caracteres de cada posição do tabuleiro presente na lista de posições

    :param pos_list: lista de posições 
    :param tiles: tabuleiro
    """
def get_stage(state:GameState) -> int:
        """
        Define o estágio do jogo com base no número de peças no tabuleiro. 
        O estágio é definido como o número de peças no tabuleiro - 4 dividido por 4, arredondado para baixo. 
        O estágio máximo é 15, que corresponde a 64 peças no tabuleiro.
        """
        num_pieces = state.board.piece_count['B'] + state.board.piece_count['W'] - 4
        stage = num_pieces // 4
        return stage

def null_conformation(configuração):
        """
        Verifica se todas nenhum caracter na configuração é '.', ou seja, uma casa vazia
        """
        for char in configuração:
            if char == '.':
                return True
        return False

def get_simple_conformation_value(configuração:str, dict:dict): 
        """
        Identifica a configuração atual da feature, busca e retorna seu valor. Versão simples da função, aplicada features que a reflexão é simplesmente a inversão da string 
        """
        ##Pegar configuração atual da feature no estado
        if null_conformation(configuração):
            return 0
        value = dict.get(configuração)
        if value != None:
            return value
        r_config = configuração[::-1]
        value = dict.get(r_config)
        if value != None:
            return value
        return 0
    
def get_complex_conformation_value(configuração:tuple, dict:dict):
    """
    Identifica a configuração atual da feature, busca e retorna seu valor. Versão complexa da função, aplicada para features que tem mais de uma casa no eixo de reflexão 
    """
    if null_conformation(configuração):
        return 0
    value = dict.get(configuração[0] + configuração[1])
    if value != None:
        return value
    r_config = configuração[0][::-1] + configuração[1]
    value = dict.get(r_config)
    if value != None:
        return value
    return 0

def parity_feature(state:GameState) -> int:
        """
        Retorna 1 se o número de peças no tabuleiro for par, e 0 se for ímpar. 
        Essa feature pode ser usada para capturar a vantagem de ter um número par ou ímpar de peças no tabuleiro, o que pode influenciar a estratégia do jogo.
        """
        num_pieces = state.board.piece_count['B'] + state.board.piece_count['W']
        return 1 if num_pieces % 2 == 0 else 0

class Train:
    partidas = 10
    def __init__(self, gamma=1.0, epsilon=0.3):
        self.gamma = gamma
        self.epsilon = epsilon
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
            with open("vectors.pkl", "rb") as file:
                self.vectors_list = pickle.load(file)
        except FileNotFoundError:
            self.vectors_list = self.init_vectors()
        return self.vectors_list
    
    def e_greedy(self, state:GameState):
        legal_moves = state.legal_moves() 
        if random.random() < self.epsilon:
            return random.choice(legal_moves)
        else:
            ##Executa uma busca com MTD(f) usando a função de avaliação atual para escolher o próximo estado
            agent_search = Agent(state, self.vectors_list)
            return agent_search.iterative_deepening(4.9)

    def update_vector(self, vector=None):
        """
        erro = r(s+1) - r(s)
        update_value = gamma*erro
        for pettern_feature, indice in pattern_features:
            configuração = configuração(pettern_feature)
            w_dict[indice][configuração] = w_dict[indice][configuração] + update_value

        """
        if vector is None:
            stage = get_stage(self.state)
            vector = self.vectors_list[stage]
        erro =  self.evaluate_state(self.next_state, vector) - self.evaluate_state(self.state, vector)
        update_value = self.gamma * erro
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
            vector[indice][configuração] = vector[indice].get(configuração, 0) + update_value

        if self.parity_feature(self.state) == 1:
            vector[-1] += update_value ##Parity_feature

    def update_vectors_soft(self):
        stage = get_stage(self.state)
        self.update_vector
        for i in range(1, 3):
            if stage + i <= 15:
                self.update_vector(self.vectors_list[stage + i])
            if stage - i >= 0:
                self.update_vector(self.vectors_list[stage - i])


            
    def update_simple_conformation(self, dict:dict, configuração, update_value):
        if null_conformation(configuração):
            return
        if configuração in dict:
            dict[configuração] += update_value
            return
        r_config = configuração[::-1]
        if r_config in dict:
            dict[r_config] += update_value
            return
        dict[configuração] = update_value
        return
    
    def update_complex_conformation(self, dict:dict, configuração, update_value):

        config = configuração[0] + configuração[1]
        if null_conformation(config):
            return
        if config in dict:
            dict[config] += update_value
            return
        r_config = configuração[0][::-1] + configuração[1]
        if r_config in dict:
            dict[r_config] += update_value
            return
        dict[config] = update_value
        return
            

    def evaluate_state(self, state:GameState, vector=None) -> float:
        """
        Esta é função r(s), a função de avaliação aplicada ao estado, ou seja, o somatório dos respectivos valores de cada ocorrência de configuração específica de cada feature do estado

        :param vector: será o vetor de dicionários com os valores a serem somados, ou seja, o vetor de pesos. Ele é necessário para acessar os valores associados as configurações específicas de cada feature. Se nenhum vetor em específico for passado será usado o vetor do estagio atual do estado. É possível passar um vetor que não seja o do estágio atual para que a estimativa de parâmetros seja feita de forma mais suave, ou seja, considerar que estágios próximos tenham valores próximos. Um mesmo estado será usado para atualizar os pesos dos vetores dos estágios d, d±1, d±2, onde d é o estágio atual do estado. 
        """
        value = 0.0
        if vector is None:
            stage = get_stage(state)
            vector = self.vectors_list[stage]
        
        value += vector[0] ##Bias

        for pattern_feature, indice in pattern_features: ##Pattern_features
            configuração = get_simple_conformation(pattern_feature, state.board.tiles)
            value += get_simple_conformation_value(configuração, vector[indice])

        for pattern_feature, indice in complex_patter_features:
            configuração = get_complex_conformation(pattern_feature, state.board.tiles) 
            value += get_complex_conformation_value(configuração, vector[indice])

        for pattern_feature, indice in non_reflexible_pattern:
            configuração = get_simple_conformation(pattern_feature, state.board.tiles)
            if null_conformation(configuração):
                continue
            returned_value = vector[indice][configuração]
            if returned_value != None:
                value += returned_value


        if parity_feature(state) == 1:
            value += vector[-1] ##Parity_feature

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
        for x in range(self.partidas):
            self.state = GameState(Board(), 'B')
            while not self.state.is_terminal():
                move = self.e_greedy(self.state)
                self.next_state = self.state.next_state(move)
                self.update_vectors_soft()
                self.state = self.next_state
            with open("vectors.pkl", "w") as file:
                pickle.dump(self.vectors_list, file, protocol=pickle.HIGHEST_PROTOCOL)
            if (x + 1)%5 == 0:
                self.epsilon *= 0.95
                self.gamma *= 0.95
                timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                log_path = f"Train_x_it_{timestamp}.txt"
                with open(log_path, "w") as file:
                    for i, vector in enumerate(self.vectors_list):
                        file.write(f"Vector:{i}\n")
                        for j, entry in enumerate(vector):
                            file.write(f"\tFeature: {j}\n")
                            if type(entry) == dict:
                                for key, value in entry:
                                    file.write(f"\t\tKey: {key}, value: {value}\n")
                            else:
                                file.write(f"\t\Value_Entry: {entry}")
            pkl_path = f"vectors_{timestamp}.pkl"
            with open(pkl_path, "w") as file:
                pickle.dump(self.vectors_list, file, protocol=pickle.HIGHEST_PROTOCOL)
                


                

                


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