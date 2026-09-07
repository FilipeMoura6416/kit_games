import random
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board
from .othello_minimax_count import evaluate_count


EVAL_TEMPLATE = [
    [100,-80,12,8,8,12,-80,100],
    [-80,-50, 0,0,0,0, -50,-80],
    [ 12,  0, 2,1,1,2,   0, 12],
    [  8,  0, 1,2,2,1,   0,  8],
    [  8,  0, 1,2,2,1,   0,  8],
    [ 12,  0, 2,1,1,2,   0, 12],
    [-80,-50, 0,0,0,0, -50,-80],
    [100,-80,12,8,8,12,-80,100]
]

SENSES = [
    [Board.UP, Board.DOWN],
    [Board.RIGHT, Board.LEFT],
    [Board.UP_RIGHT, Board.DOWN_LEFT],
    [Board.DOWN_RIGHT, Board.UP_LEFT]
]


def evaluate_custom(state, player:str) -> float:
    """
    Evaluates an othello state from the point of view of the given player. 
    """
    if state.is_terminal():        
        return evaluate_count(state, player)

    opponent = Board.opponent(player)
    
    empty_count = state.board.piece_count[Board.EMPTY]

    if empty_count > 15:
        w_template = 10
        w_mobility = 150
        w_frontier = 80
        w_immutable = 10
        w_pieces = 0
    else:
        w_template = 5
        w_mobility = 20
        w_frontier = 0
        w_immutable = 15
        w_pieces = 50

    player_template_val = 0
    my_frontier_count = 0
    opp_frontier_count = 0

    for row in range(8):
        for col in range(8):
            piece = state.board.tiles[row][col]
            if piece == Board.EMPTY:
                continue

            # Mask
            if piece == player:
                player_template_val += EVAL_TEMPLATE[row][col]
            else:
                player_template_val -= EVAL_TEMPLATE[row][col]

            # Checagem de Fronteira (O disco está adjacente a uma casa vazia?)
            is_frontier = False
            for dx, dy in Board.DIRECTIONS:
                nx, ny = col + dx, row + dy  # nx é coluna (x), ny é linha (y)
                if 0 <= nx < 8 and 0 <= ny < 8:
                    if state.board.tiles[ny][nx] == Board.EMPTY:
                        is_frontier = True
                        break

            if is_frontier:
                if piece == player:
                    my_frontier_count += 1
                else:
                    opp_frontier_count += 1

    frontier_score = opp_frontier_count - my_frontier_count

    my_moves = len(state.board.legal_moves(player))
    opp_moves = len(state.board.legal_moves(opponent))
    mobility_score = my_moves - opp_moves

    #Discos Imutáveis 
    custom = Custom_eval(state, player)
    immutable_score = custom.check_imutable_rocks()

    my_pieces = state.board.piece_count[player]
    opp_pieces = state.board.piece_count[opponent]
    piece_score = my_pieces - opp_pieces

    # Retorna o somatório dos fatores multiplicados por seus pesos da fase atual
    final_score = ((player_template_val * w_template) + (mobility_score * w_mobility) + (frontier_score * w_frontier) + (immutable_score * w_immutable) + (piece_score * w_pieces)
    )

    return final_score
        
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
        value = 12
        if read_matrix(EVAL_TEMPLATE, pos) < 0:
            value += abs(read_matrix(EVAL_TEMPLATE, pos))

        if self.get_tile(pos) == self.player:
            return value
        else:
            return -value

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

            if self.set_imutable(pontos[2]): ##Inicializa canto como imutável
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

