import pickle
from .pattern_features_by_occ import *

def converter_formato_antigo_para_novo(string_antiga, indice_feature):
    """
    Converte a string de tipos de casas do formato antigo (leitura direta do tabuleiro)
    para o novo formato padrão baseado na estrutura relativa (Canto -> Borda -> Linha Interna).
    
    :param string_antiga: str no formato "tipo1, tipo2, tipo3, ..."
    :param indice_feature: int (de 35 a 42) que identifica a ocorrência da feature
    :return: str no novo formato padronizado
    """
    # Converte a string antiga em uma lista de elementos (removendo espaços extras)
    elementos = [e.strip() for e in string_antiga.split(",")]
    
    # Se a lista não tiver os 10 elementos esperados da feature 2x5, retorna como está
    if len(elementos) != 10:
        return string_antiga

    # Dicionário de mapeamento de índices (Antigo -> Novo)
    # Cada lista mapeia qual elemento da string antiga deve ir para qual posição na string nova
    mapeamentos = {
        # 35 e 39 já estavam no formato correto devido à simetria natural do canto superior esquerdo
        35: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        39: [0, 1, 2, 3, 4, 5, 6, 7, 8, 9],
        
        # 36 (Sup. Direito Hor.): Inverte a borda longa (0 a 4) e a interna (5 a 9)
        36: [4, 3, 2, 1, 0, 9, 8, 7, 6, 5],
        
        # 37 (Inf. Esquerdo Hor.): A leitura natural já começava do canto (7,0), 
        # mas as linhas estavam invertidas verticalmente (borda interna veio primeiro na antiga)
        37: [5, 6, 7, 8, 9, 0, 1, 2, 3, 4],
        
        # 38 (Inf. Direito Hor.): Totalmente invertido (Começa no fim e vai voltando)
        38: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0],
        
        # 40 (Inf. Esquerdo Vert.): Lê de baixo para cima. Inverte blocos de 5 elementos
        40: [4, 3, 2, 1, 0, 9, 8, 7, 6, 5],
        
        # 41 (Sup. Direito Vert.): As colunas internas vieram antes na leitura antiga
        41: [5, 6, 7, 8, 9, 0, 1, 2, 3, 4],
        
        # 42 (Inf. Direito Vert.): Totalmente invertido na leitura de baixo para cima
        42: [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    }
    
    # Obtém a ordem de remapeamento para o índice fornecido
    ordem_nova = mapeamentos.get(indice_feature)
    
    if not ordem_nova:
        raise ValueError(f"Índice de feature {indice_feature} inválido para o padrão 2x5 - Corner.")
        
    # Reconstrói a lista na nova ordem estrutural
    elementos_novos = [elementos[i] for i in ordem_nova]
    
    # Junta os elementos de volta em uma string formatada
    return "".join(elementos_novos)

#Carregar vetores
vectors_path = "advsearch/rl/vectors_log/vectors.pkl"
with open(vectors_path, 'rb') as vectors_file:
    vectors_list = pickle.load(vectors_file)

new_vectors_list = []
for vector in vectors_list:
    new_vectors_list.append(list())
    new_vectors_list[-1].append(vector[0])  #Copia Bias
    for feature in pattern_features:
        new_vectors_list[-1].append(dict())
        for pattern, indice in feature:
           for key, value in vector[indice].items():
                entry = new_vectors_list[-1][-1].get(key)
                if entry == None:
                    entry = new_vectors_list[-1][-1].get(key[::-1])  # Tenta encontrar a chave invertida (para padrões reflexíveis)
                if entry == None:
                    new_vectors_list[-1][-1][key] = {"value": value["value"], "count": 1}
                else:
                    entry["value"] += (value["value"] - entry["value"]) / (entry["count"] + 1)
                    entry["count"] += 1
    new_vectors_list[-1].append(dict())
    for pattern, indice in complex_patter_features: ##Complex patterns - não é uma reflexão simples: patern[0] = casas reflexíveis, pattern[1] = casas fixas
        for key, value in vector[indice].items():
            entry = new_vectors_list[-1][-1].get(key)
            if entry == None:
                key = key[:len(pattern[0])][::-1]+key[len(pattern[0]):]  # Tenta encontrar a chave invertida (para padrões reflexíveis), invertendo apenas a parte reflexível
                entry = new_vectors_list[-1][-1].get(key)  # Tenta encontrar a chave invertida (para padrões reflexíveis)
            if entry == None:
                new_vectors_list[-1][-1][key] = {"value": value["value"], "count": 1}
            else:
                entry["value"] += (value["value"] - entry["value"]) / (entry["count"] + 1)
                entry["count"] += 1
    new_vectors_list[-1].append(dict())
    for pattern, indice in non_reflexible_pattern: ##Non-reflexible patterns - não tem reflexibilidade, então não tenta encontrar a chave invertida
        for key, value in vector[indice].items():
            key = converter_formato_antigo_para_novo(key, indice)  # Converte a chave do formato antigo para o novo formato padronizado
            entry = new_vectors_list[-1][-1].get(key)
            if entry == None:
                new_vectors_list[-1][-1][key] = {"value": value["value"], "count": 1}
            else:
                entry["value"] += (value["value"] - entry["value"]) / (entry["count"] + 1)
                entry["count"] += 1
    new_vectors_list[-1].append(dict()) #Cria espaço para a nova feature
    new_vectors_list[-1].append(vector[-1])  #Copia Valor Final

#Salvar novos vetores
new_vectors_path = "advsearch/rl/vectors_log/new_vectors.pkl"
with open(new_vectors_path, 'wb') as new_vectors_file:
    pickle.dump(new_vectors_list, new_vectors_file)

#Salvar novos vetores em txt

with open("advsearch/rl/vectors_log/new_vectors.txt", 'w') as new_vectors_file:
    for i, vector in enumerate(new_vectors_list):
        new_vectors_file.write(f"Vector: {i}\n")
        for j, feature in enumerate(vector):
            new_vectors_file.write(f"\tFeature {j}:\n")
            if type(feature) == dict:
                for key, value in feature.items():
                    new_vectors_file.write(f"\t\tKey: {key}, Value: {value['value']}, Count: {value['count']}\n")
            else:
                new_vectors_file.write(f"\t\tValue: {feature}\n")