"""
EXEMPLO DE USO DO MÓDULO 7
Mostra como:
1. Criar estruturas (regiões, cozinhas, entregadores)
2. Montar o grafo
3. Usar os algoritmos
Tudo desacoplado, pronto para integrar no main.py
"""

from modulos.modulo7 import (
    Regiao, Cozinha, Entregador, Pedido,
    GrafoLogistico, RoteadorDijkstra, InfraestruturaMinima,
    AlocadorGuloso, SimuladorCapacidade
)


def criar_sistema_logistica_exemplo():
    """
    Cria um exemplo completo de sistema logístico.
    Retorna: (grafo, cozinhas, entregadores, regioes)
    
    Isso pode ser chamado pelo main.py para inicializar tudo.
    """
    
    # PASSO 1: Criar as regiões (posições geográficas)
    regioes = {
        'rgn_centro': Regiao('rgn_centro', 'Centro', 0, 0),
        'rgn_norte': Regiao('rgn_norte', 'Região Norte', 5, 10),
        'rgn_sul': Regiao('rgn_sul', 'Região Sul', 5, -10),
        'rgn_leste': Regiao('rgn_leste', 'Região Leste', 10, 0),
    }
    
    # PASSO 2: Criar as cozinhas (posicionadas em regiões)
    cozinhas = [
        Cozinha(
            id='cz_centro',
            nome='Cozinha Central',
            regiao_id='rgn_centro',
            slots_producao=3,  # 3 pedidos simultâneos
            tempo_por_pedido=5  # 5 minutos por pedido
        ),
        Cozinha(
            id='cz_norte',
            nome='Satélite Norte',
            regiao_id='rgn_norte',
            slots_producao=2,
            tempo_por_pedido=6
        )
    ]
    
    # PASSO 3: Criar entregadores
    entregadores = [
        Entregador(
            id='entr_001',
            nome='João',
            velocidade_kmh=40,
            capacidade=2,  # Carrega 2 pedidos
            regiao_atual='rgn_centro'
        ),
        Entregador(
            id='entr_002',
            nome='Maria',
            velocidade_kmh=50,
            capacidade=3,
            regiao_atual='rgn_centro'
        ),
        Entregador(
            id='entr_003',
            nome='Pedro',
            velocidade_kmh=45,
            capacidade=2,
            regiao_atual='rgn_norte'
        )
    ]
    
    # PASSO 4: Criar grafo e adicionar nós
    grafo = GrafoLogistico()
    
    # Adicionar regiões
    for regiao in regioes.values():
        grafo.adicionar_no(regiao)
    
    # PASSO 5: Adicionar arestas (rotas) entre regiões
    # Formato: (origem, destino, tempo_minutos, custo)
    grafo.adicionar_aresta('rgn_centro', 'rgn_norte', 15, 50.0, bidirecional=True)
    grafo.adicionar_aresta('rgn_centro', 'rgn_sul', 15, 50.0, bidirecional=True)
    grafo.adicionar_aresta('rgn_centro', 'rgn_leste', 20, 60.0, bidirecional=True)
    grafo.adicionar_aresta('rgn_norte', 'rgn_leste', 25, 70.0, bidirecional=True)
    grafo.adicionar_aresta('rgn_sul', 'rgn_leste', 30, 80.0, bidirecional=True)
    
    return grafo, cozinhas, entregadores, regioes


if __name__ == '__main__':
    print("\nMÓDULO 7: O PESADELO LOGÍSTICO")
    print("Sistema de modelagem e otimização de delivery\n")
    
    # Criar sistema
    grafo, cozinhas, entregadores, regioes = criar_sistema_logistica_exemplo()
    
    print(f"Sistema criado:")
    print(f"  Regiões: {len(regioes)}")
    print(f"  Cozinhas: {len(cozinhas)}")
    print(f"  Entregadores: {len(entregadores)}")
    print(f"\n✓ Sistema pronto para uso no main.py")
