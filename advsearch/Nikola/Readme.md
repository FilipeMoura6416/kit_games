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
        A heurística customizada é uma junção de uma versão modificada da avaliação com máscara e uma contagem de peças imutáveis, ou seja, peças que não podem mais ser capturadas
    Fontes: 
        Não utilizei nenhuma fonte que tivesse implementação dessa heurística, apenas fontes como artigos de Michael Buro, criador da engine Logistello, que citam que heurística que tratam sobre a estabilidade são importantes. 
    Critério de parada:
        O agente usa uma administrador de tempo que divide o tempo restantante pelas chamadas recursivas restantes, ou seja, assim que o minimax é chamado ele receberá uma quantidade de tempo que será o tempo passado na chamada, daí em diante cada chamada recursiva "filha" recebe seu próprio horário limite que é calculado da seguinte forma: horário_limite_filho = (horário_limite_pai - horário_de_agora)/quantidade_de_filhos_restantes + horário_de_agora. Uma dos primeiros testes que cada max e min faz é testar se horário_atual >= horário_limite. 
        Ressalto que na chamada do minimax é necessário que a quantidade de tempo tenha uma folga, ou seja, se é pretendido que o agente jogue em no máximo 5 segundos é necessário chamá-lo passando 4.9 segundos. Nos testes 1 décimo de segundo de folga foi suficiente para não haver estouro de tempo. 
        Um detalhe sobre a administração de tempo é que, a forma como está implementada cria o efeito que a última camada analisada não seja a mesma para todas as ramificações. 
        Por que não aprofundamente iterativo?: Fiz testes com aprofundamente iterativo mas os resultados foram piores. Em uma análise detalhada percebi que com a divisão simples de tempo é possível analisar cerca de 1 ou 2 camadas a mais do que com aprofundamento iterativo. Teoricamente com aprofundamento iterativo seria possível reaproveitar as iterações anteriores para ordenação das ramificações a serem analisados, entretanto, acredito que por causa da heurística de avaliação não ser tão rica, tal uso não surtiu muita melhora. Concluí que o ganho gerado pelo ordenação de movimentos não foi suficiente para compensar o retrabalho do aprofundamente iterativo

    Partidas:
        Realizei três partidas consecutivas em cada um dos match's
    
        Contagem de peças X Valor posicional - Resultados: 0.5 x 2.5, Scores totais: 64 x 128
        Valor posicional X Contagem de peças - Resultados: 2 x 1, Scores totais: 118 x 74
        Contagem de peças X Heurística customizada  Resultados: 0 x 3, Scores totais: 33 x 159
        Heurística customizada X Contagem de peças: Resultados: 3 x 0, Scores totais: 174 x 18
        Valor posicional X Heurística customizada - Resultados: 1 x 2, Scores totais: 65 x 126
        Heurística customizada X Valor posicional - Resultados: 3 x 0, Scores totais: 133 x 59
        MCTS X Contagem de peças - Resultados: 2 x 1, Scores totais: 112 x 80
        Contagem de peças X MCTS - Resultados: 1 x 2, Scores totais: 125 x 67
        MCTS X Valor posicional - Resultados: 0.5 x 2.5 , Scores totais: 53 x 139
        Valor posicional X MCTS - Resultados: 3 x 0, Scores totais: 146 x 46
        MCTS X Heurística customizada - Resultados: 1 x 2, Scores totais: 75 x 117
        Heurística Customizada X MCTS - Resultados: 3 x 0, Scores totais: 144 x 48

Agente para o torneio:
    O agente para torneio ainda está em produção. Até o presente momento será um MTD(f) com aprofundamento iterativo com uma função de avaliação mais elaborada. Mais detalhes estarão disponíveis em uma relatório só para o agente a ser usado no torneio que enviarei junto ao envio do agente. 

Implementação do MCTS:
    Minha implementação do MCTS foi baseada nas videoaulas do canal do professor do Inf Anderson R. Tavares. A implementação segue a estrutra natural do MCTS: seleção, expansão, simulação e retropropagação. Como é possível ver nos resultados das partidas o desempenho do MCTS foi mediano, testei diferentes coeficiente de explitação e exploração e não houve melhora significativa do desempenho em nenhum caso. Isso se dá por ser uma implementação geral e simples. Em minhas pesquisas, encontrei um site submissão de agentes competitivos e no jogo Othello o campeão desde 2024 é um MCTS com uma rede neural para avaliação de estados. Obs: Não é possível ver o código dos agentes, a descrição do agente é do próprio autor. 

