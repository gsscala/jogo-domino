Os dois jogadores funcionam segundo o mesmo algoritmo. Basicamente, tudo gira em torno da lista "pecas".
Essa lista funciona ordenando quais peças são mais favoráveis para jogar. A ordenação das listas segue uma função lambda,
a qual, para cada tupla, retorna o somatório dos seus componentes. Isso é importante pois neste jogo é favorável jogar peças de alto valor,
uma vez que é critério de desempate. A lista "pecas" é composta pela aglutinação de três listas:
    - A primeira lista, prioritária, é formada por peças que possam travar o oponente. Ao analisar o histórico de jogadas e averiguar
    rodadas nas quais algum oponente não jogou nenhuma peça, ele olha para as extremidades do tabuleiro e determina que aquele oponente
    não tem nenhuma peça que encaixaria no tabuleiro. Nesse sentido, forma-se uma lista com peças jogáveis que terminem com aqueles números que travariam o oponente.
    Essa lista é ordenada segundo a função lambda.
    - A segunda lista é composta por peças no formato (k, k), ou seja, as denominadas "carroças", peças que têm o mesmo número nas duas extremidades.
    Essas peças são desfavoráveis devido à baixa versatilidade, portanto devem ser eliminadas rapidamente. Essa lista também é ordenada segundo a função lambda.
    - A terceira lista é composta pelo restante das peças. Também ordenada pela função lambda.
A ordem de jogadas funciona segundo a seguinte ordem de prioridade:
    1. Não há nenhuma peça no tabuleiro: retorne a primeira jogada descrita na lista de peças.
    2. Uma das extremidades está bloqueando o oponente: jogue no outro lado, se possível.
    3. Jogue a primeira jogada descrita na lista de peças.
    4. Não jogue.