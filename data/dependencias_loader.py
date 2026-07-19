import json
import os
from typing import Dict, Tuple

from estruturas.grafo import Grafo


def carregar_dependencias(caminho_arquivo: str, buscador) -> Tuple[Grafo, Dict[str, dict]]:
    #Carrega o grafo de dependências entre preparos a partir de um arquivo JSON.

    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado!")
        print("ERRO NO CARREGAMENTO DO GRAFO DE DEPENDÊNCIAS!")
        return Grafo(dirigido=True), {}

    with open(caminho_arquivo, "r", encoding="utf-8") as f:
        dados_json = json.load(f)

    grafo = Grafo(dirigido=True)
    info_vertices: Dict[str, dict] = {}

    for vertice in dados_json.get("vertices", []):
        vertice_id = vertice["id"]

        if vertice["tipo"] == "receita" and buscador.buscar_por_id(vertice_id) is None:
            print(
                f"Aviso: receita ID '{vertice_id}' citada em '{caminho_arquivo}' "
                "não foi encontrada na base de receitas. Vértice ignorado."
            )
            continue

        grafo.adicionar_vertice(vertice_id)
        info_vertices[vertice_id] = vertice

    for aresta in dados_json.get("arestas", []):
        origem, destino = aresta["origem"], aresta["destino"]

        if origem not in info_vertices or destino not in info_vertices:
            print(f"Aviso: aresta '{origem}' -> '{destino}' ignorada (vértice inexistente).")
            continue

        grafo.adicionar_aresta(origem, destino)

    return grafo, info_vertices


def nome_exibicao(vertice_id: str, info_vertices: Dict[str, dict], buscador) -> str:
    
    info = info_vertices.get(vertice_id)
    if info is None:
        return str(vertice_id)

    if info["tipo"] == "receita":
        receita = buscador.buscar_por_id(vertice_id)
        return receita.nome if receita else f"Receita desconhecida (ID {vertice_id})"

    return info.get("nome", vertice_id)
