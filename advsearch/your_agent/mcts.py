import random
import math
import time
from typing import Tuple
from ..othello.gamestate import GameState
from ..othello.board import Board

# Voce pode criar funcoes auxiliares neste arquivo
# e tambem modulos auxiliares neste pacote.
#
# Nao esqueca de renomear 'your_agent' com o nome
# do seu agente.

class MCTSNode:
    _C_PARAM = 1.4
    def __init__(self, state:GameState, parent=None, player=None, move = None):
        self.state = state
        self.player = player if player is not None else state.player
        """if state.player == None:
            raise "Error player == None"""
        self.non_expanded_moves = [] if state.is_terminal() else list(state.legal_moves())
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self.value = 0
        self.last_move = move

    def is_fully_expanded(self):
        ##Test if all possible moves have been explored
        return len(self.non_expanded_moves) == 0

    def chose_child(self) -> 'MCTSNode':
        ## Return the child with the highest UCT value
        return max(self.children, key=lambda c: c.value)

    def retroprogation(self, result):
        ## Update the node's statistics with the result of a playout
        self.visits += 1
        if result == self.player:
            self.wins += 1
        child = self
        node = self.parent
        while node:
            node.visits += 1
            if result == node.player:
                node.wins += 1
            child.calculate_UCT_value()
            child = node
            node = node.parent
    
    def calculate_UCT_value(self) -> None:
        ##Calculate the UCT value of the node
        if self.parent:
            self.value = self.wins / self.visits + 2 * self._C_PARAM * math.sqrt(math.log(self.parent.visits) / self.visits)
    
    def expand(self) -> 'MCTSNode':
        ## Create a new child node by applying the given move to the current state. If no move is given, choose a random move from the non-expanded moves.
        
        move = self.non_expanded_moves.pop()
        new_state = self.state.next_state(move)
        child_node = MCTSNode(new_state, parent=self, player=self.player, move=move)
        self.children.append(child_node)
        return child_node
    
    def playout(self) -> float:
        """
        Simulates a random playout from the given state until the game ends.
        Returns the score of the player who made the move in this state.

        :param state: state to simulate
        :return: score of the player who made the move in this state
        """
        state = self.state
        while not state.is_terminal():
            moves = list(state.board.legal_moves(state.player))
            move = random.choice(moves)
            state = state.next_state(move)
        
        return state.winner()
    
def MCTS(root_state: GameState, time_limit=4.9) -> Tuple[int, int]:
    """
    Performs MCTS starting from the given root state and returns the best move found within the time limit.

    :param root_state: the initial game state to start MCTS from
    :param time_limit: the time limit for MCTS in seconds
    :return: (int, int) tuple with x, y coordinates of the best move found
    """
    ## Inicialization of the MCTS algorithm
    root_node = MCTSNode(root_state)
    start_time = time.time()
    
    while time.time() - start_time < time_limit:
        #Selection
        node = root_node
        while node.is_fully_expanded() and not node.state.is_terminal():
            node = node.chose_child()
            
        #Expand
        if not node.state.is_terminal():
            node = node.expand()

        #Simulation
        result = node.playout()

        #Back-propagation
        node.retroprogation(result)

    best_child = max(root_node.children, key=lambda c: c.visits)
    print("Visits: ", root_node.visits)
    return best_child.last_move

def make_move(state:GameState) -> Tuple[int, int]:
    """
    Returns a move for the given game state. 
    The game is not specified, but this is MCTS and should handle any game, since
    their implementation has the same interface.

    :param state: state to make the move
    :return: (int, int) tuple with x, y coordinates of the move (remember: 0 is the first row/column)
    """
    return MCTS(state)






