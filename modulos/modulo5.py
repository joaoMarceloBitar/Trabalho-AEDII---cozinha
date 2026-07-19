#modulo 5

from typing import Iterable, List, NamedTuple, Optional

from algoritmos.topologica import (
    CicloDetectadoError,
    ancestrais,
    detectar_ciclo,
    ordem_para_alvos,
    ordenar_ou_explicar,
    subgrafo_induzido,
)
from data.dependencias_loader import nome_exibicao
from estruturas.grafo import Grafo

class ResultadoSequencia(NamedTuple):
    sucesso: bool
    ordem: Optional[List[str]]
    mensagem_erro: Optional[str]


class ResultadoInconsistencia(NamedTuple):
    tem_erro: bool
    ciclo: Optional[List[str]]


class ResultadoAncestrais(NamedTuple):
    sucesso: bool
    preparos: Optional[List[str]]
    mensagem_erro: Optional[str]


def sequencia_producao_menu(
    grafo: Grafo, info_vertices: dict, buscador, ids_alvo: Iterable[str]
) -> ResultadoSequencia:
    #Consulta 1: Qual a sequência correta para produzir o menu do dia?  
    try:
        ordem_ids = ordem_para_alvos(grafo, ids_alvo)
    except ValueError as erro:
        return ResultadoSequencia(sucesso=False, ordem=None, mensagem_erro=str(erro))
    except CicloDetectadoError as erro:
        ciclo_nomes = [nome_exibicao(v, info_vertices, buscador) for v in erro.ciclo]
        mensagem = (
            "Não é possível produzir esse menu: há um erro de cadastro nas "
            "dependências, formando um ciclo:\n  "
            + " -> ".join(ciclo_nomes)
        )
        return ResultadoSequencia(sucesso=False, ordem=None, mensagem_erro=mensagem)

    ordem_nomes = [nome_exibicao(v, info_vertices, buscador) for v in ordem_ids]
    return ResultadoSequencia(sucesso=True, ordem=ordem_nomes, mensagem_erro=None)


def detectar_erro_dependencia(grafo: Grafo, info_vertices: dict, buscador) -> ResultadoInconsistencia:
    #Consulta 2: Existe algum erro de dependência?

    ciclo_ids = detectar_ciclo(grafo)
    if ciclo_ids is None:
        return ResultadoInconsistencia(tem_erro=False, ciclo=None)

    ciclo_nomes = [nome_exibicao(v, info_vertices, buscador) for v in ciclo_ids]
    return ResultadoInconsistencia(tem_erro=True, ciclo=ciclo_nomes)


def preparos_antecedentes(
    grafo: Grafo, info_vertices: dict, buscador, id_receita: str
) -> ResultadoAncestrais:
    #Consulta 3: Quais preparos precisam ser concluídos antes da receita X?
    
    try:
        ancestrais_ids = ancestrais(grafo, id_receita)
    except ValueError as erro:
        return ResultadoAncestrais(sucesso=False, preparos=None, mensagem_erro=str(erro))

    if not ancestrais_ids:
        return ResultadoAncestrais(sucesso=True, preparos=[], mensagem_erro=None)

    subgrafo = subgrafo_induzido(grafo, ancestrais_ids)

    try:
        ordem_ids = ordenar_ou_explicar(subgrafo)
    except CicloDetectadoError as erro:
        ciclo_nomes = [nome_exibicao(v, info_vertices, buscador) for v in erro.ciclo]
        mensagem = (
            "Erro de cadastro: os próprios preparos antecedentes formam um ciclo:\n  "
            + " -> ".join(ciclo_nomes)
        )
        return ResultadoAncestrais(sucesso=False, preparos=None, mensagem_erro=mensagem)

    nomes = [nome_exibicao(v, info_vertices, buscador) for v in ordem_ids]
    return ResultadoAncestrais(sucesso=True, preparos=nomes, mensagem_erro=None)
