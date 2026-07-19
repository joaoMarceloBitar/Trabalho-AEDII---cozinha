from typing import Dict, Hashable, Iterator, List, Tuple


class Grafo:
    # Grafo genérico implementado com lista de adjacência (dict de dict).
    # Suporta grafos dirigidos ou não-dirigidos e arestas com peso.

    def __init__(self, dirigido: bool = True):
        #Inicializa um grafo vazio.
        self.dirigido = dirigido
        self._adjacencia: Dict[Hashable, Dict[Hashable, float]] = {}
        self._grau_entrada: Dict[Hashable, int] = {}

    def adicionar_vertice(self, vertice: Hashable) -> None:
     
        if vertice not in self._adjacencia:
            self._adjacencia[vertice] = {}
            self._grau_entrada[vertice] = 0

    def adicionar_aresta(self, origem: Hashable, destino: Hashable, peso: float = 1) -> None:
        #Adiciona uma aresta origem -> destino (e o inverso, se não-dirigido).

        #Cria os vértices envolvidos automaticamente caso ainda não existam.
        #Se a aresta já existir, o peso é atualizado (não duplica grau de
        #entrada).

        self.adicionar_vertice(origem)
        self.adicionar_vertice(destino)

        if destino not in self._adjacencia[origem]:
            self._grau_entrada[destino] += 1
        self._adjacencia[origem][destino] = peso

        if not self.dirigido and origem != destino:
            if origem not in self._adjacencia[destino]:
                self._grau_entrada[origem] += 1
            self._adjacencia[destino][origem] = peso

    def vizinhos(self, vertice: Hashable) -> List[Tuple[Hashable, float]]:
        #Devolve os vizinhos de saída de `vertice` com seus pesos.
        return list(self._adjacencia.get(vertice, {}).items())

    def grau_entrada(self, vertice: Hashable) -> int:
        #Devolve o grau de entrada de `vertice` (nº de arestas que chegam nele).
        return self._grau_entrada.get(vertice, 0)

    def transposto(self) -> "Grafo":
        #Constrói o grafo transposto (todas as arestas com sentido invertido).

        #Usado para calcular ancestrais de um vértice: um preparo X é
        #ancestral de Y no grafo original se, e somente se, X é alcançável a
        #partir de Y no grafo transposto.

        transposto = Grafo(dirigido=self.dirigido)
        for vertice in self._adjacencia:
            transposto.adicionar_vertice(vertice)
        for origem, destino, peso in self.arestas():
            transposto.adicionar_aresta(destino, origem, peso)
        return transposto

    def arestas(self) -> Iterator[Tuple[Hashable, Hashable, float]]:
        #Itera sobre as arestas do grafo.
        #Em grafos não-dirigidos, cada aresta é reportada uma única vez.

        vistas = set()
        for origem, vizinhos in self._adjacencia.items():
            for destino, peso in vizinhos.items():
                if not self.dirigido:
                    chave = frozenset((origem, destino))
                    if chave in vistas:
                        continue
                    vistas.add(chave)
                yield (origem, destino, peso)

    def __len__(self) -> int:
        #Número de vértices do grafo.
        return len(self._adjacencia)

    def __iter__(self) -> Iterator[Hashable]:
        #Itera sobre os vértices do grafo.
        return iter(self._adjacencia)

    def __contains__(self, vertice: Hashable) -> bool:
        #Verifica se `vertice` existe no grafo.
        return vertice in self._adjacencia
