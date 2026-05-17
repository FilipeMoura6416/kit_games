import subprocess
import xml.etree.ElementTree as ET

string_command = {
    "MCTS X Heurística customizada": "python server.py othello advsearch/Nikola/mcts.py advsearch/Nikola/othello_minimax_custom.py",
    "Heurística customizada X MCTS": "python server.py othello advsearch/Nikola/othello_minimax_custom.py advsearch/Nikola/mcts.py",

}
log_path = "C:/Users/lfsmo/Superpasta/Ufrgs/Bolsa_Game_AI/kit_games/advsearch/Nikola/resultados.txt"
for key, command in string_command.items():
    command = command.split()
    dict_resultados = {"B" : {"result": 0, "score": 0}, "W" : {"result": 0, "score": 0}}
    for i in range(3):
        print(f"Rodando partida {key} - {i}")
        resultado = subprocess.run(command, capture_output=True, text=True)
        arvore = ET.parse("C:\\Users\\lfsmo\\Superpasta\\Ufrgs\\Bolsa_Game_AI\\kit_games\\results.xml")
        for player in arvore.findall("player"):
            if player.get("result") == "win":
                dict_resultados[player.get("color")]["result"] += 1
            elif player.get("result") == "draw":
                dict_resultados[player.get("color")]["result"] += 0.5
            dict_resultados[player.get("color")]["score"] += int(player.get("score"))
        
    with open(log_path, 'a') as log_file:
        log_file.write(f"\n\nResultados para {key}: ")
        for color, resultado in dict_resultados.items():
            log_file.write(f"\nJogador {color} - Vitórias: {resultado['result']} - Pontuação total: {resultado['score']}")

print("Todas as partidas foram executadas")
