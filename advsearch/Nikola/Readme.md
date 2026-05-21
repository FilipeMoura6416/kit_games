python server.py tttm advsearch\Nikola\tttm_minimax.py  advsearch\randomplayer\agent.py -d 30
**Relatório:**

Luís Filipe Santos de Moura, 588077, Turma A
Bibliotecas: Nenhuma biblioteca adicional é necessária

Resultado da sua avaliação da poda alfa-beta no tic-tac-toe misere:
    (i) O minimax sempre ganha ou empata jogando contra o randomplayer?
        Sim, em todas as partidas contra o randomplayer resultaram em empate ou vitória de Nikola
    (ii) O minimax sempre empata consigo mesmo?
        Sim
    (iii) O minimax não perde para você quando você usa a sua melhor estratégia?
        Sim

    Como mais um passo para confirmar que o agente está jogando tttm perfeitamente, durante os testes imprimi cada camada de forma identada em um arquivo de forma que foi possível verificar a estrutura esperada. Na primeira camada há 9 ramificações, na segunda camada cada ramificação se ramifica em 8 e assim por diante até que se encontre um estado terminal, assim como o esperado.
    Dado tais considerações temos grandes indicativos que o agente joga tttm perfeitamente

Othello:
    
    Heurística customizada:
        A heurística customizada é uma junção de uma versão modificada da avaliação com máscara e uma contagem de peças imutáveis, ou seja, peças que não podem mais ser capturadas. Essa verificação de peças imutáveis é feita da seguinte forma: Se houver uma peça no canto, configura como imutável, avança nas duas bordas adjacentes ao canto (chamemos borda_a e borda_b) verificando até onde há peças iguais a do canto consecutivamente, todas essas são configuradas como imutáveis, a peça mais distantes de cada uma das duas bordas serão limites, chamemos limite_a e limite_b. Após isso avança nas diagonais que uma ponta está na borda_a e a outra está na borda_b. Definirei aqui o que chamarei de Direções: {(Up,down), (left, right), (up_right, down_left), (up_left, down_right)}, cada direção tem dois sentidos. Percorre cada elemento da diagonal verificando se para cada uma das 4 direções existe ao menos uma peça adjacente que seja imutável, se sim a peça analisada também é imutável. As diagonais são limitadas por limite_a e limite_b. Esse processo se repete para cada canto 
    Fontes: 
        Não utilizei nenhuma fonte que tivesse implementação dessa heurística, apenas fontes como artigos de Michael Buro, criador da engine Logistello, que citam que heurística que tratam sobre a estabilidade são importantes. 

    Partidas:
    
        Contagem de peças X Valor posicional:       0 X 1,      Scores: 28 X 36
        Valor posicional X Contagem de peças:       0 X 1,      Scores: 26 X 37
        Contagem de peças X Heurística customizada: 0 X 1,      Scores: 27 X 37
        Heurística customizada X Contagem de peças: 1 X 0,      Scores: 58 X 6
        Valor posicional X Heurística customizada:  0 X 1,      Scores: 29 X 35
        Heurística customizada X Valor posicional:  1 X 0,      Scores: 45 X 19
        MCTS X Contagem de peças:                   1 X 0,      Scores: 38 X 26
        Contagem de peças X MCTS:                   0 X 1,      Scores: 27 X 37
        MCTS X Valor posicional:                    1 X 0,      Scores: 41 X 23
        Valor posicional X MCTS:                    0.5 X 0.5,  Scores: 32 X 32
        MCTS X Heurística customizada:              1 X 0,      Scores: 37 X 27
        Heurística customizada X MCTS:              1 X 0,      Scores: 40 X 24 

        Totais por implementação:
        Implementação       Resultado   Score total
        Heurística Custom   5/6         242
        MCTS                4.5/6       209
        Valor Posicional    1.5/6       165
        Contagem de peças   1/6         151




Implementação do MCTS:
    Minha implementação do MCTS foi baseada nas videoaulas do canal do professor do Inf Anderson R. Tavares. A implementação segue a estrutra natural do MCTS: seleção, expansão, simulação e retropropagação. Como é possível ver nos resultados das partidas o desempenho do MCTS foi relativamente bom, entretanto esse resultado é fortemente influenciado pelo fato da implementação aqui apresentada do Minimax é com profundidade máxima, o que dificulta uma comparação justa entre os algoritmos. Ressalto que fiz outros teste usando controle dinâmico de tempo e MCTS acaba por não ser um competidor tão bom quanto apresentado nas partidas aqui descritas. Testei diferentes coeficiente de explitação e exploração e não houve melhora significativa do desempenho em nenhum caso. Isso se dá por ser uma implementação geral e simples. Em minhas pesquisas, encontrei um site submissão de agentes competitivos e no jogo Othello o campeão desde 2024 é um MCTS com uma rede neural para avaliação de estados. Obs: Não é possível ver o código dos agentes, a descrição do agente é do próprio autor. 

Implementação mais bem-sucedida

