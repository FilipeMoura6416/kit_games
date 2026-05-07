if __name__ == "__main__":
    from ..othello.board import Board
    from ..othello.gamestate import GameState
    from .othello_minimax_custom import evaluate_custom, make_move as mm_minimax
    from .othello_minimax_mask import evaluate_mask
    from .negamax_tt_id import make_move as mm_negamax

    string_board = """........\n........\n....W...\n..BBBB..\n...BB...\nWWWWWB..\n....W...\n........"""

    board:Board = Board().from_string(string_board)
    print(board.decorated_str(colors=False))
    state = GameState(board, 'B')
    value = evaluate_custom(state, 'B')
    print(value)
    value2 = evaluate_mask(state, 'B')
    print(value2)
    mm_negamax(state)
    mm_minimax(state)
