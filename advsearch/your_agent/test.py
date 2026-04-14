if __name__ == "__main__":
    from ..othello.board import Board
    from ..othello.gamestate import GameState
    from .othello_minimax_custom import evaluate_custom
    from .othello_minimax_mask import evaluate_mask

    board:Board = Board()
    board.tiles = [
                ##Evaluating state at depth 6 player: W my_player: W
						['.', 'W', 'W', 'W', 'W', 'W', '.', '.'],
						['W', '.', 'W', 'B', 'W', 'W', '.', '.'],
						['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W'],
						['W', 'W', 'W', 'B', 'W', 'W', 'W', 'W'],
						['W', 'W', 'B', 'W', 'B', 'W', '.', 'W'],
						['W', 'B', 'W', 'W', 'W', 'B', 'W', 'W'],
						['B', 'B', 'B', 'B', 'B', 'B', 'B', '.'],
						['W', '.', 'W', 'W', 'W', 'W', '.', '.']
						##Evaluated state: 417
            ]
    state = GameState(board, 'B')
    value = evaluate_custom(state, 'B')
    print(value)
    value2 = evaluate_mask(state, 'B')
    print(value2)