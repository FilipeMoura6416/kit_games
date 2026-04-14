import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .minimax import minimax_move
from .othello_minimax_count import evaluate_count
from .minimax import log_path

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

EVAL_TEMPLATE = [
    [100,-40,10,8,8,10,-40,100],
    [-40,-50, 1,1,1,1, -50,-40],
    [ 10,  1, 2,1,1,2,   1, 10],
    [  8,  1, 1,2,2,1,   1,  8],
    [  8,  1, 1,2,2,1,   1,  8],
    [ 10,  1, 2,1,1,2,   1, 10],
    [-40,-50, 1,1,1,1, -50,-40],
    [100,-40,10,8,8,10,-40,100]
]

SENSES = [
    [Board.UP, Board.DOWN],
    [Board.RIGHT, Board.LEFT],
    [Board.UP_RIGHT, Board.DOWN_LEFT],
    [Board.DOWN_RIGHT, Board.UP_LEFT]
]


def make_move(state) -> Tuple[int, int]:
    """
    Returns a move for the given game state
    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """

    # o codigo abaixo apenas retorna um movimento aleatorio valido para
    # a primeira jogada 
    # Remova-o e coloque uma chamada para o minimax_move (que vc implementara' no modulo minimax).
    # A chamada a minimax_move deve receber sua funcao evaluate como parametro.

    return minimax_move(state, 4.9, evaluate_custom)

def evaluate_custom(state, player:str, state_is_terminal=False) -> float:
        """
        Evaluates an othello state from the point of view of the given player. 
        If the state is terminal, returns its utility. 
        If non-terminal, returns an estimate of its value based on your custom heuristic
        :param state: state to evaluate (instance of GameState)
        :param player: player to evaluate the state for (B or W)
        """
        if not state_is_terminal:        
            player_value = 0
            for row in range(1, len(state.board.tiles) - 1):
                for cell in range(1, len(state.board.tiles[row]) - 1):
                    if state.board.tiles[row][cell] == player:
                        player_value += EVAL_TEMPLATE[row][cell]
                    elif state.board.tiles[row][cell] != Board.EMPTY:
                        player_value -= EVAL_TEMPLATE[row][cell]

            custom = Custom_eval(state, player)
            player_value += custom.check_imutable_rocks()

            return player_value
        else:
            return evaluate_count(state, player)
        
class Custom_eval:
        
    def __init__(self, state, player):

        self.tiles = state.board.tiles
        self.player = player
        self.immutable = [[False] * 8 for x in range(8)]
        self.corners = [(0,0), (0,7), (7,7), (7,0)]
                        
                      
    def check_and_set_slot(self, pos, corner):
        """
        Check if a given position is a imutable rock, assums the check order is correct, if not, indeterminate behavior
        return true only if a new imutable rock is detected if not return false
        """
        if read_matrix(self.immutable, pos):
            return False
        if self.get_tile(pos) != self.get_tile(corner):
            return False
        for sense in SENSES:
            if not (self.is_my_imutable(deslocate_point(pos, sense[0]), corner) or self.is_my_imutable(deslocate_point(pos, sense[1]), corner)):
                return False
            
        self.immutable[pos[0]][pos[1]] = True
        return True


    def is_my_imutable(self, pos, corner):
        return read_matrix(self.immutable, pos) and self.get_tile(pos) == self.get_tile(corner)

    def set_imutable(self, pos):
        """
        Try set position, if the position was already true return false else return true 
        """
        if read_matrix(self.immutable, pos):
            return False 
        else:
            self.immutable[pos[0]][pos[1]] = True
            return True

    def imutable_value(self, pos):
        if self.get_tile(pos) == self.player:
            return 1
        else:
            return -1

    def get_tile(self, pos):
        return self.tiles[pos[0]][pos[1]]
    def calc_limit(self, pontos):
        dx0 = abs(pontos[0][0]-pontos[2][0])
        dy0 = abs(pontos[0][1]-pontos[2][1])
        dx1 = abs(pontos[1][0]-pontos[2][0])
        dy1 = abs(pontos[1][1]-pontos[2][1])
        if max(dx0,dy0) > max(dx1, dy1):
            self.far_end = pontos[0]
            self.near_end = pontos[1]
        else:
            self.far_end = pontos[1]
            self.near_end = pontos[0]
        return (max(dx0, dx1), max(dy0, dy1))
    
    def check_imutable_rocks(self):
        """
        Imutables: matriz de booleanos onde cada posição representa se a casa é imutável
        ideia geral: começar em cada um dos cantos, inicializar imutáveis a partir da coluna e linha do canto atual
        Guardar o imutável mais distante do canto seja na linha ou na coluna
        Percorrer todas as diagonais até o imutável mais distante:
            Testar cada casa
                Se houver uma peça e 
                Se para verdade para todas as direções, então a casa é imutável:
                    entre as duas casas adjacentes em uma direção ao menos uma casa for imutável
                
        """
        
        immutables_value_sum = 0

        for corner in range(4):
            pontos = list()
            pontos.append(self.corners[corner]) #end1
            pontos.append(self.corners[(corner + 2)%4]) #end2
            pontos.append(self.corners[(corner + 1)%4]) #start
            

            if self.get_tile(pontos[2]) == Board.EMPTY:
                continue

            if self.set_imutable(pontos[2]):
                immutables_value_sum += self.imutable_value(pontos[2])

            ## Inicializa na coluna e na linha do canto em questão
            for i in range(2):
                end = pontos[i]
                dxy = direction(pontos[2], end)
                current = deslocate_point(pontos[2], dxy)
                pontos[i] = pontos[2] ##pontos[i] passará a guardar o imutável mais distante, inicializando no próprio start
                while self.get_tile(current) == self.get_tile(pontos[2]): #pontos[2] = start = canto
                    pontos[i] = current
                    if self.set_imutable(current):
                        immutables_value_sum += self.imutable_value(current)
                    if current == end:
                        break
                    current = deslocate_point(current, dxy)
                    

            ##Percorre as diagonais limitado pelo mais distante da linha e o da coluna
            
            limit = self.calc_limit(pontos)

            dxy = direction(pontos[2], self.far_end)
            diag_dxy = direction(self.far_end, self.near_end)
            if diag_dxy[0] == 0 or diag_dxy[1] == 0:
                continue
            current = deslocate_point(pontos[2], dxy)
            while is_before(pontos[2], limit, current):
                diagonal_current = current ## elemento atual da diagonal, não a diagonal atual
                diagonal_next = deslocate_point(diagonal_current, diag_dxy)
                while is_before(pontos[2], limit, diagonal_next) and is_in_bounds(diagonal_next):
                    diagonal_current = diagonal_next
                    if self.check_and_set_slot(diagonal_current, pontos[2]):
                        immutables_value_sum += self.imutable_value(diagonal_current)
                    diagonal_next = deslocate_point(diagonal_next, diag_dxy)
                current = deslocate_point(current, dxy)

        return immutables_value_sum
      


def is_before(start, limit, point):
    return abs(point[0] - start[0]) <= limit[0] and abs(point[1] - start[1]) <= limit[1] 

def read_matrix(matrix, pos):
    return matrix[pos[0]][pos[1]]

def deslocate_point(pos, deslocamento):
      return (pos[0] + deslocamento[0], pos[1] + deslocamento[1])

def get_pos_mask(pos):
      return EVAL_TEMPLATE[pos[0]][pos[1]]

def direction(start, end):
    dist_y = end[0] - start[0]
    delta_y = dist_y/abs(dist_y) if dist_y != 0 else 0
    dist_x = end[1] - start[1]
    delta_x = dist_x/abs(dist_x) if dist_x != 0 else 0
    return (int(delta_y), int(delta_x))

def d1_distance(point1, point2):
    """Returns the 1 dimension distance"""
    return max(abs(point1[0]-point2[0]), abs(point1[1] -point2[1]))
def is_in_bounds(pos):
    return 0 <= pos[0] < 8 and 0 <= pos[1] < 8



"""
    Algoritmos descartados ou não finalizados

      Pseudo-código
      Imutables: matriz para guardar peças conhecidamente imutáveis
      Começar computando as bordas
      Defnições: 
        Movimentações:
            V: 
                Executada apenas se:
                    A movimentação anterior foi do tipo v e
                    Na movimentação v anterior a distância dist(end1, start) == dist(end2,start)
                Consiste em:
                    A partir do start percorrer no máximo até end1 verificando imutáveis
                    A partir do start percorrer no máximo até end2 verificando imutáveis
                        Em ambos os casos parar se testar uma casa e esta não for imutável

            Onda:
                Executada se:
                    A movimentação anterior foi do tipo v e
                    Na movimentação v anterior a distância dist(end1, start) != dist(end2,start) ou
                    A movimentação anterior foi do tipo onda


    def eval_edges(state, player) -> float:
        player_value = 0
        adversario = 'W' if player == 'B' else 'B'

        ##Testa primeira linha
        linha_completa = 1
        if state.board.tiles[0][1] == player:
                        player_value += EVAL_TEMPLATE[0][1]
        elif state.board.tiles[0][1] != Board.EMPTY:
                player_value -= EVAL_TEMPLATE[0][1]
        for j in range(2, 7):
            if not (state.board.tiles[0][j] == state.board.tiles[0][j - 1] and state.board.tiles[0][j] != Board.EMPTY) :
                linha_completa = 0
            if state.board.tiles[0][j] == player:
                        player_value += EVAL_TEMPLATE[0][j]
            elif state.board.tiles[0][j] != Board.EMPTY:
                player_value -= EVAL_TEMPLATE[0][j]

        if linha_completa:
            if state.board.tiles[0][1] == player and ((state.board.tiles[0][0] != adversario) ^ (state.board.tiles[0][7] != adversario)):
                player_value += 60
            else:
                player_value -= 60

        ##Testa ultima linha
        linha_completa = 1
        if state.board.tiles[7][1] == player:
                        player_value += EVAL_TEMPLATE[7][1]
        elif state.board.tiles[7][1] != Board.EMPTY:
            player_value -= EVAL_TEMPLATE[7][1]
        for j in range(2, 7):
            if not (state.board.tiles[7][j] == state.board.tiles[7][j - 1] and state.board.tiles[7][j] != Board.EMPTY):
                linha_completa = 0
            if state.board.tiles[7][j] == player:
                        player_value += EVAL_TEMPLATE[7][j]
            elif state.board.tiles[7][j] != Board.EMPTY:
                player_value -= EVAL_TEMPLATE[7][j]
        if linha_completa:
            if state.board.tiles[7][1] == player and ((state.board.tiles[7][0] != adversario) ^ (state.board.tiles[7][7] != adversario)):
                player_value += 60
            else:
                player_value -= 60

        ##Testa primeira coluna
        linha_completa = 1
        if state.board.tiles[1][0] == player:
                        player_value += EVAL_TEMPLATE[1][0]
        elif state.board.tiles[1][0] != Board.EMPTY:
            player_value -= EVAL_TEMPLATE[1][0]
        for j in range(2, 7):
            if not (state.board.tiles[j][0] == state.board.tiles[j-1][0] and state.board.tiles[j][0] != Board.EMPTY):
                linha_completa = 0
            if state.board.tiles[j][0] == player:
                        player_value += EVAL_TEMPLATE[j][0]
            elif state.board.tiles[j][0] != Board.EMPTY:
                player_value -= EVAL_TEMPLATE[j][0]
        if linha_completa:
            if state.board.tiles[1][0] == player and ((state.board.tiles[0][0] != adversario) ^ (state.board.tiles[7][0] != adversario)):
                player_value += 60
            else:
                player_value -= 60
            ##Testa ultima coluna

        linha_completa = 1
        if state.board.tiles[1][7] == player:
                        player_value += EVAL_TEMPLATE[1][7]
        elif state.board.tiles[1][7] != Board.EMPTY:
            player_value -= EVAL_TEMPLATE[1][7]
        for j in range(2, 7):
            if not (state.board.tiles[j][7] == state.board.tiles[j-1][7] and state.board.tiles[j][7] != Board.EMPTY):
                linha_completa = 0
            if state.board.tiles[j][7] == player:
                        player_value += EVAL_TEMPLATE[j][7]
            elif state.board.tiles[j][7] != Board.EMPTY:
                player_value -= EVAL_TEMPLATE[j][7]
        if linha_completa:
            if state.board.tiles[1][7] == player and ((state.board.tiles[0][7] != adversario) ^ (state.board.tiles[7][7] != adversario)):
                player_value += 60
            else:
                player_value -= 60

        return player_value

    def evaluate_edges(state, player) -> float:
        
        ## Inicializa lista de corners
        corners = [(0,0), (0,7), (7,7), (7,0)]
        ## Percorre formando vetores
        ## Verifica a distância das coordenadas x e y
        ## Enquanto distancia > 0 
        #   Decrementa
        #   Verifica
        player_value = 0
        for dot in range(len(corners)):
            start = corners[dot]
            end = corners[(dot + 1)%4]
            y_dist = end[0] - start[0]
            x_dist = end[1] - start[1]
            linha_completa = True
            direction = (0,0)
            if y_dist > 1:
                direction[0] = y_dist/abs(y_dist)
            if x_dist > 1:
                direction[1] = x_dist/abs(x_dist)
            current = (start[0] + direction[0], start[1] + direction[1])
            current_tile = ''
            while current[0] + direction[0] != end[0] or current[1] + direction[1] != end[1] :
                next = (current[0] + direction[0], current[1] + direction[1])
                current_tile = get_position(state, current)
                if  current_tile != get_position(state, next):
                    linha_completa = False
                if current_tile == player:
                    player_value += get_pos_mask(current)
                elif current_tile != Board.EMPTY:
                    player_value -+  get_pos_mask(current)
                current = next
            if linha_completa and get_position(state, current) != Board.EMPTY:
                opponent = Board.opponent(player)
                ##if current_tile == player and ((get_position(start) != opponent) ^ (get_position(end) != opponent)):
                        
        return player_value
      """