if __name__ == "__main__":
    from ..othello.board import Board
    from ..othello.gamestate import GameState
    from .MTD_f_tiny_log import Agent, vectors_list
    from ..fixed_rl.high_quality_function import *
    from .MTD_f_heavy_log import make_move as mm_heavy

    string_board = ""
    with open("advsearch\\your_agent\\board.txt", 'r') as board_file:
        lines = board_file.readlines()
        for i in range(1, len(lines)):
            for j in range(2, len(lines[i])):
                if lines[i][j] not in "0123456789 *":
                    string_board += lines[i][j]

    board = Board().from_string(string_board)
    state = GameState(board, 'B')
    # agent = Agent(state, vectors_list)
    # print(f"Val w: {agent.eval_func(state, 'W')}")
    # train = Train()
    # print(f"Train evaluate_state: {train.evaluate_state(state, player='W')}")
    print(f"Heavy: {mm_heavy(state)}")
