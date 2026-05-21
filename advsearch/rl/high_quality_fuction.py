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

"""

import pickle
from ..othello.gamestate import GameState
from ..othello.board import Board
import random
from ..your_agent.MTD_f_no_log import Agent


def pattern(pos_list, tiles):
    conformation = ""
    for pos in pos_list:
        x, y = pos
        conformation += tiles[x][y]
    return conformation

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
    ([(0,0), (0,1), (0,2), (0,3), (0,4), (0,5), (0,6), (0,7), (1,1), (1,6)], 31), ## Borda Superior
    ([(7,0), (7,1), (7,2), (7,3), (7,4), (7,5), (7,6), (7,7), (6,1), (6,6)], 32), ## Borda Inferior
    ([(0,0), (1,0), (2,0), (3,0), (4,0), (5,0), (6,0), (7,0), (1,1), (6,1)], 33), ## Borda Esquerda
    ([(0,7), (1,7), (2,7), (3,7), (4,7), (5,7), (6,7), (7,7), (1,6), (6,6)], 34), ## Borda Direita

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

    ## ==================== 3x3 - CORNER ====================
    ([(0,0), (0,1), (0,2), (1,0), (1,1), (1,2), (2,0), (2,1), (2,2)], 43),         ## Sup. Esquerdo
    ([(0,5), (0,6), (0,7), (1,5), (1,6), (1,7), (2,5), (2,6), (2,7)], 44),         ## Sup. Direito
    ([(5,0), (5,1), (5,2), (6,0), (6,1), (6,2), (7,0), (7,1), (7,2)], 45),         ## Inf. Esquerdo
    ([(5,5), (5,6), (5,7), (6,5), (6,6), (6,7), (7,5), (7,6), (7,7)], 46)          ## Inf. Direito
]

class Train:
    def __init__(self, alpha, gamma, epsilon=0.3):
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

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
            agent_search = Agent(state)
            return agent_search.iterative_deepening(4.9)


    
    def run_training(self):
        

if __name__ == "__main__":
