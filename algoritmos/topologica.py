from collections import deque
from typing import Hashable, Iterable, List, Optional, Set

from estruturas.grafo import Grafo


class CicloDetectadoError(Exception):
    #Erro levantado quando não existe ordem topológica válida por causa de um ciclo.

    def __init__(self, ciclo: List[Hashable]):
        self.ciclo = ciclo
        caminho = " -> ".join(str(v) for v in ciclo)
        super().__init__(f"Ciclo de dependências detectado: {caminho}")


def detectar_ciclo(grafo: Grafo) -> Optional[List[Hashable]]:
    #Procura um ciclo no grafo dirigido usando DFS iterativa com 3 cores.
    #branco - nao visitado
    #cinza - visitado
    #preto - processado
    
    BRANCO, CINZA, PRETO = 0, 1, 2
    cor = {vertice: BRANCO for vertice in grafo}

    for origem in grafo:
        if cor[origem] != BRANCO:
            continue

        pilha = [[origem, iter(grafo.vizinhos(origem))]]
        caminho = [origem]
        cor[origem] = CINZA

        while pilha:
            vertice_atual, iterador_vizinhos = pilha[-1]
            proximo = next(iterador_vizinhos, None)

            if proximo is None:
                cor[vertice_atual] = PRETO
                pilha.pop()
                caminho.pop()
                continue

            vizinho, _peso = proximo

            if cor[vizinho] == BRANCO:
                cor[vizinho] = CINZA
                caminho.append(vizinho)
                pilha.append([vizinho, iter(grafo.vizinhos(vizinho))])
            elif cor[vizinho] == CINZA:
                indice = caminho.index(vizinho)
                return caminho[indice:] + [vizinho]
            # se PRETO, o vizinho já foi totalmente processado e não fecha ciclo

    return None


def ordenacao_topologica(grafo: Grafo) -> Optional[List[Hashable]]:
    #Calcula uma ordenação topológica pelo algoritmo de Kahn.
    #Mantém o grau de entrada de cada vértice e vai retirando da fila os
    #vértices com grau de entrada zero, decrementando o grau dos seus
    #vizinhos conforme são "produzidos".

    grau_entrada = {vertice: grafo.grau_entrada(vertice) for vertice in grafo}
    fila = deque(vertice for vertice in grafo if grau_entrada[vertice] == 0)
    ordem: List[Hashable] = []

    while fila:
        vertice = fila.popleft()
        ordem.append(vertice)
        for vizinho, _peso in grafo.vizinhos(vertice):
            grau_entrada[vizinho] -= 1
            if grau_entrada[vizinho] == 0:
                fila.append(vizinho)

    if len(ordem) != len(grafo):
        return None

    return ordem


def ordenar_ou_explicar(grafo: Grafo) -> List[Hashable]:
    #Tenta ordenar topologicamente o grafo; se houver ciclo, explica qual é.
    
    ordem = ordenacao_topologica(grafo)
    if ordem is None:
        ciclo = detectar_ciclo(grafo)
        raise CicloDetectadoError(ciclo)
    return ordem


def _alcancaveis_no_transposto(transposto: Grafo, iniciais: Iterable[Hashable]) -> Set[Hashable]:
    #Busca (DFS iterativa) todos os vértices alcançáveis a partir de `iniciais` no grafo transposto.

    #Como o transposto inverte todas as arestas, "alcançável a partir de X no
    #transposto" equivale a "ancestral de X no grafo original" — ou seja,
    #"precisa estar pronto antes de X".

    visitados = set(iniciais)
    pilha = list(iniciais)

    while pilha:
        atual = pilha.pop()
        for vizinho, _peso in transposto.vizinhos(atual):
            if vizinho not in visitados:
                visitados.add(vizinho)
                pilha.append(vizinho)

    return visitados


def subgrafo_induzido(grafo: Grafo, vertices: Iterable[Hashable]) -> Grafo:
    #Constrói o subgrafo induzido por um conjunto de vértices.
    #O subgrafo contém exatamente os vértices informados e apenas as arestas
    #do grafo original cujas duas pontas pertencem a esse conjunto.

    vertices = set(vertices)
    subgrafo = Grafo(dirigido=grafo.dirigido)
    for vertice in vertices:
        subgrafo.adicionar_vertice(vertice)
    for origem, destino, peso in grafo.arestas():
        if origem in vertices and destino in vertices:
            subgrafo.adicionar_aresta(origem, destino, peso)
    return subgrafo


def ancestrais(grafo: Grafo, vertice: Hashable) -> Set[Hashable]:
    #Calcula o fecho transitivo dos ancestrais de `vertice` (preparos que precisam vir antes dele).

    
    if vertice not in grafo:
        raise ValueError(f"Preparo '{vertice}' não encontrado no grafo de dependências.")

    transposto = grafo.transposto()
    alcancaveis = _alcancaveis_no_transposto(transposto, [vertice])
    alcancaveis.discard(vertice)
    return alcancaveis


def ordem_para_alvos(grafo: Grafo, alvos: Iterable[Hashable]) -> List[Hashable]:
    #Calcula a ordem de produção restrita ao necessário para um conjunto de receitas-alvo.

    #Restringe o grafo ao subgrafo induzido pelos alvos e seus ancestrais
    #e roda a ordenação topológica apenas nesse subgrafo.

    alvos = list(alvos)
    ausentes = [alvo for alvo in alvos if alvo not in grafo]
    if ausentes:
        nomes = ", ".join(str(a) for a in ausentes)
        raise ValueError(f"Preparo(s) não cadastrado(s) no grafo de dependências: {nomes}")

    transposto = grafo.transposto()
    necessarios = _alcancaveis_no_transposto(transposto, alvos)
    subgrafo = subgrafo_induzido(grafo, necessarios)

    return ordenar_ou_explicar(subgrafo)
