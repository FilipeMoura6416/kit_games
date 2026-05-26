from ..othello.gamestate import GameState
from ..othello.board import Board
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
