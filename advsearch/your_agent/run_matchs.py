import datetime
import xml.etree.ElementTree as ET
import subprocess
import time

def get_agents_scores():
    
    tree = ET.parse('results.xml')
    root = tree.getroot()
    contents = root.findall('player')
    print(contents)
    for agent, content in enumerate(contents):
        print(f"{int(content.get('score'))}")

get_agents_scores()
agents = {"MTD_f_to_rl": "advsearch\\your_agent\\MTD_f_to_rl.py", "Tiny_log": "advsearch\\your_agent\\MTD_f_tiny_log.py"}
itens = list(agents.items())
time_stamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
log_path = f"matchs_log_{time_stamp}.txt"
match_number = 4
pasta_kit_games = "C:\\Users\\lfsmo\\Superpasta\\Ufrgs\\Bolsa_Game_AI\\kit_games"
for i in range(len(itens) - 1):
    for j in range(i + 1, len(itens)):
        for h in range(2):
            player_b = i if h % 2 == 0 else j
            player_w = j if h % 2 == 0 else i
            print(f"Match between {itens[player_b][0]} and {itens[player_w][0]}")
            agents_scores = [0, 0]
            for match in range(match_number):
                start = time.time()
                print(f"Match {match + 1}/{match_number}")
                try:
                    start_subpro = time.time()
                    resultado = subprocess.run(f'python server.py othello {itens[player_b][1]} {itens[player_w][1]}"', capture_output=True, text=True, shell=True)
                    print(f"Time taken to run match: {time.time() - start_subpro}")
                except Exception as e:
                    print(f"Error occurred while running subprocess: {e}")
                    raise e
                resultado = resultado.stdout.splitlines()
                resultado = resultado[-4:-1]
                for line in resultado:
                    print(line)
                tree = ET.parse('results.xml')
                root = tree.getroot()
                for agent, content in enumerate(root.findall('player')):
                    agents_scores[agent] += int(content.get('score'))
                print(f"Finished match time taken: {time.time() - start}")
            with open(log_path, "a") as log_file:
                log_file.write(f"Match between {itens[player_b][0]} and {itens[player_w][0]}\n")
                log_file.write(f"Final score: {agents_scores[0]} - {agents_scores[1]}\n\n")