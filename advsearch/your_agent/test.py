if __name__ == "__main__":
    from ..othello.board import Board
    from ..othello.gamestate import GameState
    from .othello_minimax_custom import evaluate_custom

    board:Board = Board()
    board.tiles = [
                    ['.', '.', 'B', 'W', 'W', '.', 'B', 'B'],
                    ['W', '.', 'W', 'W', '.', '.', 'B', 'B'],
                    ['W', 'W', 'B', 'W', 'B', 'W', 'B', 'B'],
                    ['W', 'W', 'B', 'W', 'W', 'B', 'B', 'B'],
                    ['W', 'B', 'B', 'W', 'W', 'W', 'B', 'B'],
                    ['W', 'B', 'B', 'W', 'W', 'W', 'B', 'B'],
                    ['.', 'B', 'B', 'W', 'B', 'B', 'W', 'B'],
                    ['W', 'W', 'W', 'W', 'W', 'W', 'W', 'W']
            ]
    state = GameState(board, 'W')
    value = evaluate_custom(state, 'W')
    print(value)