from ..rl.pattern_features import *
from ..rl.high_quality_function import *
from ..rl.aid_functions import *

string_board = ""
with open("advsearch\\your_agent\\board.txt", 'r') as board_file:
    lines = board_file.readlines()
    for i in range(1, len(lines)):
        for j in range(2, len(lines[i])):
            if lines[i][j] not in "0123456789 *":
                string_board += lines[i][j]

board:Board = Board().from_string(string_board)
print(board.decorated_str(colors=False))
state = GameState(board, 'B')
for i in range(4):
    string1, string2 = get_complex_conformation(complex_patter_features[i][0], state.board.tiles)
    print(f"Configurações da feature {string1}{string2} e sua reflexão {string1[::-1]}{string2}")
