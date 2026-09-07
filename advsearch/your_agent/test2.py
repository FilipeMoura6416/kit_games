if __name__ == "__main__":
    from ..othello.board import Board
    from ..othello.gamestate import GameState
    from .MTD_f_tiny_log import Agent, vectors_list
    from ..fixed_rl.high_quality_function import *

    string_board = ""
    with open("advsearch\\your_agent\\board2.txt", 'r') as board_file:
        lines = board_file.readlines()
        for i in range(0, len(lines)):
            for j in range(0, len(lines[i])):
                if lines[i][j] not in "0123456789 *":
                    string_board += lines[i][j]

    board = Board().from_string(string_board)
    print(board.decorated_str(colors=False))
    state = GameState(board, 'W')
    
    agent = Agent(state, vectors_list)
    print(f"Tiny_log Val w: {agent.eval_func(state, 'W')}")
    train = Train()
    print(f"Train evaluate_state: {train.evaluate_state(state, player="W")}")
