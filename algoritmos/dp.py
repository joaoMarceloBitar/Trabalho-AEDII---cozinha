#algoritmos de programação dinâmica - Mochila 0/1 (Módulo 6)

from typing import Callable, List, Sequence, TypeVar


Item = TypeVar("Item")


def mochila_01(
    itens: Sequence[Item],
    capacidade: int,
    peso_de: Callable[[Item], int],
    valor_de: Callable[[Item], float],
) -> List[List[float]]:
    # Resolve a Mochila 0/1 por programação dinâmica bottom-up.

    n = len(itens)
    # Tabela (n+1) x (capacidade+1) inicializada com 0 (casos-base).
    dp: List[List[float]] = [[0.0] * (capacidade + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        peso = peso_de(itens[i - 1])
        valor = valor_de(itens[i - 1])
        for c in range(capacidade + 1):
            # Opção 1: não incluir o item i -> herda a linha de cima.
            melhor = dp[i - 1][c]
            # Opção 2: incluir o item i, se ele couber na capacidade c.
            if peso <= c:
                candidato = dp[i - 1][c - peso] + valor
                if candidato > melhor:
                    melhor = candidato
            dp[i][c] = melhor

    return dp


def reconstruir_solucao(
    tabela: List[List[float]],
    itens: Sequence[Item],
    capacidade: int,
    peso_de: Callable[[Item], int],
) -> List[Item]:
    # Reconstrói quais itens compõem o ótimo, percorrendo a tabela de trás p/ frente.
    
    escolhidos: List[Item] = []
    c = capacidade
    for i in range(len(itens), 0, -1):
        # Se o valor mudou da linha i-1 para a linha i, o item i foi incluído.
        if tabela[i][c] != tabela[i - 1][c]:
            item = itens[i - 1]
            escolhidos.append(item)
            c -= peso_de(item)

    escolhidos.reverse()  # devolve na ordem original dos itens
    return escolhidos


def mochila_2d(
    itens: Sequence[Item],
    cap_tempo: int,
    cap_orcamento: int,
    tempo_de: Callable[[Item], int],
    custo_de: Callable[[Item], int],
    valor_de: Callable[[Item], float],
) -> List[List[List[float]]]:
    #Mochila 0/1 com DUAS restrições simultâneas (tempo E orçamento).

    n = len(itens)
    dp: List[List[List[float]]] = [
        [[0.0] * (cap_orcamento + 1) for _ in range(cap_tempo + 1)]
        for _ in range(n + 1)
    ]

    for i in range(1, n + 1):
        pt = tempo_de(itens[i - 1])
        pc = custo_de(itens[i - 1])
        valor = valor_de(itens[i - 1])
        for t in range(cap_tempo + 1):
            for c in range(cap_orcamento + 1):
                melhor = dp[i - 1][t][c]  # não leva o item i
                if pt <= t and pc <= c:   # cabe nas duas restrições?
                    candidato = dp[i - 1][t - pt][c - pc] + valor
                    if candidato > melhor:
                        melhor = candidato
                dp[i][t][c] = melhor

    return dp


def reconstruir_solucao_2d(
    tabela: List[List[List[float]]],
    itens: Sequence[Item],
    cap_tempo: int,
    cap_orcamento: int,
    tempo_de: Callable[[Item], int],
    custo_de: Callable[[Item], int],
) -> List[Item]:
    
    escolhidos: List[Item] = []
    t, c = cap_tempo, cap_orcamento
    for i in range(len(itens), 0, -1):
        if tabela[i][t][c] != tabela[i - 1][t][c]:
            item = itens[i - 1]
            escolhidos.append(item)
            t -= tempo_de(item)
            c -= custo_de(item)

    escolhidos.reverse()
    return escolhidos


def mochila_greedy(
    itens: Sequence[Item],
    capacidade: int,
    peso_de: Callable[[Item], int],
    valor_de: Callable[[Item], float],
) -> List[Item]:
    #Heurística GULOSA por razão valor/peso — NÃO é a solução do Módulo 6.

    # Razão valor/peso; max(peso, 1) evita divisão por zero para peso 0.
    ordenados = sorted(
        itens, key=lambda item: valor_de(item) / max(peso_de(item), 1), reverse=True
    )

    escolhidos: List[Item] = []
    usado = 0
    for item in ordenados:
        peso = peso_de(item)
        if usado + peso <= capacidade:
            escolhidos.append(item)
            usado += peso

    return escolhidos
