if __name__ == "__main__":
    from ..othello.board import Board
    from ..othello.gamestate import GameState
    from .othello_minimax_custom import evaluate_custom, make_move as mm_minimax
    from .othello_minimax_mask import evaluate_mask
    from .negamax_tt_id import make_move as mm_negamax

    string_board = ""
    with open("advsearch\\your_agent\\board.txt", 'r') as board_file:
        for lines in board_file.readlines():
            string_board += lines

    board:Board = Board().from_string(string_board)
    print(board.decorated_str(colors=False))
    state = GameState(board, 'W')
    value = evaluate_custom(state, 'W')
    print(value)
    value2 = evaluate_mask(state, 'W')
    print(value2)
    print(f"Negamax return move: {mm_negamax(state)}")
    print(f"Minimax return move: {mm_minimax(state)}")
    print("teste finalizado")
