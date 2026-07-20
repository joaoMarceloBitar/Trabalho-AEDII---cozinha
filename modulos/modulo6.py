#modulo 6 - O Menu Degustação VIP (Otimização por Mochila 0/1)

import math
from typing import Callable, List, NamedTuple, Optional, Sequence, Set

from algoritmos.dp import (
    mochila_01,
    mochila_2d,
    reconstruir_solucao,
    reconstruir_solucao_2d,
)
from estruturas.hash import TabelaHash
from receita.receita import Receita

LIMIAR_RARIDADE = 3
ESCALA_AVALIACAO = 10 
ESCALA_MONETARIA = 100  


class ResultadoMenu(NamedTuple):
    sucesso: bool
    receitas: Optional[List[Receita]]
    valor_total: Optional[float]
    candidatos_considerados: int
    mensagem_erro: Optional[str]

# 1. RARIDADE POR FREQUÊNCIA

def contar_frequencia_ingredientes(receitas: Sequence[Receita]) -> TabelaHash:

    contagem = TabelaHash(tamanho_tabela=200)
    for receita in receitas:
        for ingrediente in {ing.lower() for ing in receita.ingredientes}:
            atual = contagem.buscar(ingrediente)
            contagem.inserir(ingrediente, 1 if atual is None else atual + 1)
    return contagem


def identificar_ingredientes_raros(
    receitas: Sequence[Receita], limiar: int = LIMIAR_RARIDADE
) -> Set[str]:
    #Identifica os ingredientes raros
    contagem = contar_frequencia_ingredientes(receitas)
    distintos = {ing.lower() for r in receitas for ing in r.ingredientes}
    return {ing for ing in distintos if contagem.buscar(ing) < limiar}


def filtrar_ingredientes_disponiveis(
    receitas: Sequence[Receita], disponiveis: Set[str]
) -> List[Receita]:
    #Mantém só as receitas que tem todos os ingredientes disponiveis
    disponiveis = {ing.lower() for ing in disponiveis}
    return [
        r for r in receitas
        if all(ing.lower() in disponiveis for ing in r.ingredientes)
    ]


def filtrar_limite_raros(
    receitas: Sequence[Receita], ingredientes_raros: Set[str], max_raros: int
) -> List[Receita]:
   
    resultado = []
    for r in receitas:
        qtd_raros = sum(1 for ing in {i.lower() for i in r.ingredientes} if ing in ingredientes_raros)
        if qtd_raros <= max_raros:
            resultado.append(r)
    return resultado


def filtrar_capacidade_equipe(
    receitas: Sequence[Receita], dificuldades_permitidas: Set[str]
) -> List[Receita]:
    
    permitidas = {d.lower() for d in dificuldades_permitidas}
    return [r for r in receitas if str(r.dificuldade or "").lower() in permitidas]


def aplicar_filtros(
    receitas: Sequence[Receita],
    disponiveis: Optional[Set[str]] = None,
    max_raros: Optional[int] = None,
    dificuldades_permitidas: Optional[Set[str]] = None,
    limiar_raridade: int = LIMIAR_RARIDADE,
) -> List[Receita]:
    
    candidatos = list(receitas)

    if dificuldades_permitidas is not None:
        candidatos = filtrar_capacidade_equipe(candidatos, dificuldades_permitidas)

    if disponiveis is not None:
        candidatos = filtrar_ingredientes_disponiveis(candidatos, disponiveis)

    if max_raros is not None:
        raros = identificar_ingredientes_raros(receitas, limiar_raridade)
        candidatos = filtrar_limite_raros(candidatos, raros, max_raros)

    return candidatos



def _funcoes_criterio(criterio: str):
   
    criterio = criterio.lower()
    if criterio == "lucro":
        return (lambda r: round(r.lucro * ESCALA_MONETARIA), lambda r: r.lucro, "lucro (R$)")
    if criterio == "avaliacao":
        return (lambda r: round(r.avaliacao * ESCALA_AVALIACAO), lambda r: r.avaliacao, "soma de avaliações")
    if criterio == "popularidade":
        return (lambda r: int(r.popularidade), lambda r: r.popularidade, "popularidade")
    raise ValueError(f"Critério desconhecido: '{criterio}'. Use lucro, avaliacao ou popularidade.")


def _custo_inteiro(receita: Receita) -> int:

    return math.ceil(receita.custo)


def otimizar_menu(
    candidatos: Sequence[Receita],
    capacidade: int,
    peso_de: Callable[[Receita], int],
    valor_de: Callable[[Receita], int],
    valor_real: Callable[[Receita], float],
) -> ResultadoMenu:

    if capacidade <= 0:
        return ResultadoMenu(False, None, None, 0, "Capacidade/limite inválido: informe um valor positivo.")
    if not candidatos:
        return ResultadoMenu(False, None, None, 0, "Nenhuma receita elegível após os filtros aplicados.")

    tabela = mochila_01(candidatos, capacidade, peso_de, valor_de)
    escolhidos = reconstruir_solucao(tabela, candidatos, capacidade, peso_de)

    if not escolhidos:
        return ResultadoMenu(False, None, None, len(candidatos),
                             "Nenhuma receita cabe na capacidade informada.")

    valor_total = sum(valor_real(r) for r in escolhidos)
    return ResultadoMenu(True, escolhidos, valor_total, len(candidatos), None)


def otimizar_menu_2d(
    candidatos: Sequence[Receita],
    cap_tempo: int,
    cap_orcamento: int,
    valor_de: Callable[[Receita], int],
    valor_real: Callable[[Receita], float],
) -> ResultadoMenu:
    
    if cap_tempo <= 0 or cap_orcamento <= 0:
        return ResultadoMenu(False, None, None, 0, "Tempo e orçamento devem ser positivos.")
    if not candidatos:
        return ResultadoMenu(False, None, None, 0, "Nenhuma receita elegível após os filtros aplicados.")

    tabela = mochila_2d(candidatos, cap_tempo, cap_orcamento, lambda r: r.tempo, _custo_inteiro, valor_de)
    escolhidos = reconstruir_solucao_2d(tabela, candidatos, cap_tempo, cap_orcamento, lambda r: r.tempo, _custo_inteiro)

    if not escolhidos:
        return ResultadoMenu(False, None, None, len(candidatos),
                             "Nenhuma receita cabe nas restrições de tempo e orçamento.")

    valor_total = sum(valor_real(r) for r in escolhidos)
    return ResultadoMenu(True, escolhidos, valor_total, len(candidatos), None)



def consulta_melhor_menu_por_orcamento(
    receitas: Sequence[Receita],
    orcamento: float,
    criterio: str = "lucro",
    disponiveis: Optional[Set[str]] = None,
    max_raros: Optional[int] = None,
    dificuldades_permitidas: Optional[Set[str]] = None,
) -> ResultadoMenu:
   
    if orcamento is None or orcamento <= 0:
        return ResultadoMenu(False, None, None, 0, "Orçamento inválido: informe um valor positivo.")
    try:
        valor_de, valor_real, _ = _funcoes_criterio(criterio)
    except ValueError as erro:
        return ResultadoMenu(False, None, None, 0, str(erro))

    candidatos = aplicar_filtros(receitas, disponiveis, max_raros, dificuldades_permitidas)
    return otimizar_menu(candidatos, int(orcamento), _custo_inteiro, valor_de, valor_real)


def consulta_melhor_menu_por_tempo(
    receitas: Sequence[Receita],
    tempo_max_minutos: int,
    criterio: str = "avaliacao",
    disponiveis: Optional[Set[str]] = None,
    max_raros: Optional[int] = None,
    dificuldades_permitidas: Optional[Set[str]] = None,
) -> ResultadoMenu:

    if tempo_max_minutos is None or tempo_max_minutos <= 0:
        return ResultadoMenu(False, None, None, 0, "Tempo máximo inválido: informe um valor positivo.")
    try:
        valor_de, valor_real, _ = _funcoes_criterio(criterio)
    except ValueError as erro:
        return ResultadoMenu(False, None, None, 0, str(erro))

    candidatos = aplicar_filtros(receitas, disponiveis, max_raros, dificuldades_permitidas)
    return otimizar_menu(candidatos, int(tempo_max_minutos), lambda r: r.tempo, valor_de, valor_real)


def consulta_maximizar_avaliacao_por_tempo(
    receitas: Sequence[Receita],
    tempo_max_minutos: int,
    disponiveis: Optional[Set[str]] = None,
    max_raros: Optional[int] = None,
    dificuldades_permitidas: Optional[Set[str]] = None,
) -> ResultadoMenu:

    return consulta_melhor_menu_por_tempo(
        receitas, tempo_max_minutos, "avaliacao", disponiveis, max_raros, dificuldades_permitidas
    )


def consulta_maior_lucro_ingredientes_disponiveis(
    receitas: Sequence[Receita],
    disponiveis: Set[str],
    orcamento: float,
    max_raros: Optional[int] = None,
    dificuldades_permitidas: Optional[Set[str]] = None,
) -> ResultadoMenu:

    if not disponiveis:
        return ResultadoMenu(False, None, None, 0, "Informe ao menos um ingrediente disponível em estoque.")
    return consulta_melhor_menu_por_orcamento(
        receitas, orcamento, "lucro", disponiveis, max_raros, dificuldades_permitidas
    )


def consulta_menu_por_tempo_e_orcamento(
    receitas: Sequence[Receita],
    tempo_max_minutos: int,
    orcamento: float,
    criterio: str = "lucro",
    disponiveis: Optional[Set[str]] = None,
    max_raros: Optional[int] = None,
    dificuldades_permitidas: Optional[Set[str]] = None,
) -> ResultadoMenu:

    if tempo_max_minutos is None or tempo_max_minutos <= 0 or orcamento is None or orcamento <= 0:
        return ResultadoMenu(False, None, None, 0, "Tempo e orçamento devem ser positivos.")
    try:
        valor_de, valor_real, _ = _funcoes_criterio(criterio)
    except ValueError as erro:
        return ResultadoMenu(False, None, None, 0, str(erro))

    candidatos = aplicar_filtros(receitas, disponiveis, max_raros, dificuldades_permitidas)
    return otimizar_menu_2d(candidatos, int(tempo_max_minutos), int(orcamento), valor_de, valor_real)
