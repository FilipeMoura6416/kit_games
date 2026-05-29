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
    
def get_stage(state:GameState) -> int:
        """
        Define o estágio do jogo com base no número de peças no tabuleiro. 
        O estágio é definido como o número de peças no tabuleiro - 4 dividido por 4, arredondado para baixo. 
        O estágio máximo é 15, que corresponde a 64 peças no tabuleiro.
        """
        return 0

def null_conformation(configuração):
        """
        Verifica se todas os caracteres na configuração são '.', ou seja, uma casa vazia
        """
        for char in configuração:
            if char == 'W' or char == 'B':
                return False
        return True

def get_simple_conformation_value(configuração:str, dict:dict): 
        """
        Identifica a configuração atual da feature, busca e retorna seu valor. Versão simples da função, aplicada features que a reflexão é simplesmente a inversão da string 
        """
        ##Pegar configuração atual da feature no estado
        if null_conformation(configuração):
            return 0
        entry = dict.get(configuração)
        if entry != None:
            return entry["value"]
        r_config = configuração[::-1]
        entry = dict.get(r_config)
        if entry != None:
            return entry["value"]
        return 0
    
