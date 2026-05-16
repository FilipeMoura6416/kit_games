if __name__ == "__main__":
    from ..othello.board import Board
    from ..othello.gamestate import GameState
    from .othello_minimax_custom import evaluate_custom, make_move as mm_minimax
    from .othello_minimax_mask import evaluate_mask
    from .negamax_tt_id import make_move as mm_negamax
    from .MTD_f import make_move as MTDF_move

    string_board = ""
    with open("advsearch\\your_agent\\board.txt", 'r') as board_file:
        lines = board_file.readlines()
        for i in range(1, len(lines)):
            for j in range(2, len(lines[i])):
                if lines[i][j] not in "0123456789 *":
                    string_board += lines[i][j]

    ##board:Board = Board().from_string(string_board)
    board:Board = Board().from_string(string_board)
    print(board.decorated_str(colors=False))
    state = GameState(board, 'W')
    value = evaluate_custom(state, 'B')
    print(f"Value: {value}\n")
    """ returned_move = MTDF_move(state)
    print(f"MTD(f) retornou o movimento: {returned_move}")
    print("teste finalizado") """
