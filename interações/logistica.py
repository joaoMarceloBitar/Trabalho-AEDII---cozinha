"""
MODO LOGÍSTICA (Módulo 7)
Interação para otimização de delivery e análise de gargalos

Funcionalidades:
- Consultar rotas (Dijkstra)
- Alocar pedidos (Guloso)
- Analisar capacidade máxima
- Simular pico
- Calcular infraestrutura mínima (Prim MST)
"""

import os
from modulos.modulo7 import (
    RoteadorDijkstra,
    AlocadorGuloso,
    SimuladorCapacidade,
    InfraestruturaMinima,
    Pedido
)


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def modoLogistica(grafo, cozinhas, entregadores, regioes):
    """
    Modo principal para análise de logística e otimização de delivery.
    
    Args:
        grafo: GrafoLogistico com regiões e rotas
        cozinhas: lista de Cozinha
        entregadores: lista de Entregador
        regioes: dict de regiões disponíveis
    """
    while True:
        limpar_tela()
        print("=" * 60)
        print("MÓDULO 7 — O PESADELO LOGÍSTICO")
        print("Sistema de Otimização de Delivery")
        print("=" * 60)
        print("\n1. Consultar Rota (Dijkstra)")
        print("2. Alocar Pedidos (Algoritmo Guloso)")
        print("3. Capacidade Máxima do Sistema")
        print("4. Simular Cenário de Pico")
        print("5. Infraestrutura Mínima (Prim MST)")
        print("0. Voltar aos Modos de Interação")
        print("\n" + "-" * 60)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            consultar_rota(grafo)
        elif opcao == "2":
            alocar_pedidos(grafo, cozinhas, entregadores, regioes)
        elif opcao == "3":
            capacidade_maxima(cozinhas, entregadores)
        elif opcao == "4":
            simular_pico(grafo, cozinhas, entregadores, regioes)
        elif opcao == "5":
            infraestrutura_minima(grafo)
        elif opcao == "0":
            break
        else:
            print("\n⚠️  Opção inválida!")
            input("\nPressione Enter para voltar...")


def consultar_rota(grafo):
    """Consulta a rota mais rápida entre dois pontos usando Dijkstra."""
    limpar_tela()
    print("-" * 60)
    print("CONSULTAR ROTA (Dijkstra)")
    print("-" * 60)
    
    # Listar regiões disponíveis
    regioes_ids = list(grafo.nos.keys())
    print(f"\nRegiões disponíveis: {', '.join(regioes_ids)}")
    
    origem = input("\nDigite a região de origem: ").strip()
    destino = input("Digite a região de destino: ").strip()
    
    # Validar
    if origem not in grafo.nos:
        print(f"\n⚠️  Região '{origem}' não encontrada!")
        input("\nPressione Enter para voltar...")
        return
    
    if destino not in grafo.nos:
        print(f"\n⚠️  Região '{destino}' não encontrada!")
        input("\nPressione Enter para voltar...")
        return
    
    # Calcular rota
    roteador = RoteadorDijkstra(grafo)
    tempo, caminho = roteador.caminho_mais_curto(origem, destino)
    
    # Exibir resultado
    if not caminho:
        print(f"\n⚠️  Sem rota possível entre '{origem}' e '{destino}'!")
    else:
        print(f"\n✓ Rota encontrada:")
        print(f"  Caminho: {' → '.join(caminho)}")
        print(f"  Tempo total: {tempo:.1f} minutos")
    
    input("\nPressione Enter para voltar...")


def alocar_pedidos(grafo, cozinhas, entregadores, regioes):
    """Aloca pedidos de forma eficiente usando algoritmo guloso."""
    limpar_tela()
    print("-" * 60)
    print("ALOCAR PEDIDOS (Algoritmo Guloso)")
    print("-" * 60)
    
    try:
        num_pedidos = int(input("\nQuantos pedidos deseja alocar? "))
        if num_pedidos <= 0:
            print("⚠️  Quantidade inválida!")
            input("\nPressione Enter para voltar...")
            return
    except ValueError:
        print("⚠️  Digite um número válido!")
        input("\nPressione Enter para voltar...")
        return
    
    # Criar pedidos
    pedidos = []
    regioes_ids = list(grafo.nos.keys())
    
    for i in range(num_pedidos):
        regiao = regioes_ids[i % len(regioes_ids)]
        tempo_prep = 5 + (i % 5)  # 5 a 9 minutos
        prioridade = 1 if i < 2 else 0  # Primeiros 2 urgentes
        
        pedido = Pedido(
            id=f'ped_{i+1:04d}',
            regiao_destino=regiao,
            tempo_preparo=tempo_prep,
            prioridade=prioridade
        )
        pedidos.append(pedido)
    
    # Alocar
    alocador = AlocadorGuloso(grafo, cozinhas, entregadores)
    alocacoes, nao_alocados = alocador.alocar(pedidos)
    
    # Resultado
    print(f"\n✓ Resultado da alocação:")
    print(f"  Total de pedidos: {num_pedidos}")
    print(f"  Pedidos alocados: {len(alocacoes)} ✓")
    print(f"  Pedidos não alocados: {len(nao_alocados)} ✗ (sem capacidade)")
    
    # Mostrar detalhes (até 10 primeiros)
    if len(alocacoes) > 0:
        print(f"\n  Detalhes dos alocados:")
        for ped_id, (cz_id, entr_id) in list(alocacoes.items())[:10]:
            cozinha = next((c for c in cozinhas if c.id == cz_id), None)
            entr = next((e for e in entregadores if e.id == entr_id), None)
            
            cz_nome = cozinha.nome if cozinha else cz_id
            entr_nome = entr.nome if entr else entr_id
            
            print(f"    {ped_id} → Cozinha: {cz_nome}, Entregador: {entr_nome}")
        
        if len(alocacoes) > 10:
            print(f"    ... e mais {len(alocacoes) - 10} pedidos")
    
    input("\nPressione Enter para voltar...")


def capacidade_maxima(cozinhas, entregadores):
    """Mostra a capacidade máxima de atendimento do sistema."""
    limpar_tela()
    print("-" * 60)
    print("CAPACIDADE MÁXIMA DO SISTEMA")
    print("-" * 60)
    
    # Capacidade de produção
    print("\n📊 Capacidade de Produção:")
    cap_producao_total = 0
    
    for cozinha in cozinhas:
        cap_cozinha = (cozinha.slots_producao * 60) / cozinha.tempo_por_pedido
        cap_producao_total += cap_cozinha
        
        print(f"\n  Cozinha: {cozinha.nome}")
        print(f"    Slots paralelos: {cozinha.slots_producao}")
        print(f"    Tempo por pedido: {cozinha.tempo_por_pedido} min")
        print(f"    Capacidade: {cap_cozinha:.2f} pedidos/hora")
    
    cap_producao_minutos = cap_producao_total / 60
    
    # Capacidade de entrega
    print("\n📊 Capacidade de Entrega:")
    cap_entrega_total = 0
    
    for entregador in entregadores:
        cap_entregador = entregador.capacidade * 6  # 6 viagens/hora (10 min cada)
        cap_entrega_total += cap_entregador
        
        print(f"\n  Entregador: {entregador.nome}")
        print(f"    Capacidade por viagem: {entregador.capacidade} pedidos")
        print(f"    Capacidade: {cap_entregador} pedidos/hora")
    
    cap_entrega_minutos = cap_entrega_total / 60
    
    # Identificar gargalo
    if cap_producao_minutos < cap_entrega_minutos:
        gargalo = "PRODUÇÃO"
        valor = cap_producao_minutos
        descricao = "As cozinhas são o gargalo"
    elif cap_entrega_minutos < cap_producao_minutos:
        gargalo = "ENTREGA"
        valor = cap_entrega_minutos
        descricao = "Os entregadores são o gargalo"
    else:
        gargalo = "BALANCEADO"
        valor = cap_producao_minutos
        descricao = "Sistema bem balanceado"
    
    print(f"\n{'='*60}")
    print(f"📈 Capacidade de Produção: {cap_producao_minutos:.3f} pedidos/min")
    print(f"📦 Capacidade de Entrega: {cap_entrega_minutos:.3f} pedidos/min")
    print(f"\n⚠️  GARGALO: {gargalo}")
    print(f"   {descricao}")
    print(f"\n✓ Capacidade Máxima: {valor:.3f} pedidos/min ({valor*60:.1f} pedidos/hora)")
    print(f"{'='*60}")
    
    input("\nPressione Enter para voltar...")


def simular_pico(grafo, cozinhas, entregadores, regioes):
    """Simula cenário de pico com muitos pedidos simultâneos."""
    limpar_tela()
    print("-" * 60)
    print("SIMULAÇÃO DE PICO")
    print("-" * 60)
    
    try:
        num_pedidos = int(input("\nQuantos pedidos em pico deseja simular? "))
        if num_pedidos <= 0:
            print("⚠️  Quantidade inválida!")
            input("\nPressione Enter para voltar...")
            return
    except ValueError:
        print("⚠️  Digite um número válido!")
        input("\nPressione Enter para voltar...")
        return
    
    # Criar pedidos de pico
    pedidos_pico = []
    regioes_ids = list(grafo.nos.keys())
    
    for i in range(num_pedidos):
        regiao = regioes_ids[i % len(regioes_ids)]
        pedido = Pedido(
            id=f'pico_{i+1:04d}',
            regiao_destino=regiao,
            tempo_preparo=5,
            prioridade=0
        )
        pedidos_pico.append(pedido)
    
    # Simular
    alocador = AlocadorGuloso(grafo, cozinhas, entregadores)
    simulador = SimuladorCapacidade(alocador, cozinhas, entregadores, grafo)
    resultado = simulador.simular_pico(pedidos_pico)
    
    # Exibir resultado
    print(f"\n✓ Resultado da simulação de pico:")
    print(f"\n  Cenário: {num_pedidos} pedidos chegando simultaneamente")
    print(f"  Pedidos atendidos: {resultado['alocados']} ✓")
    print(f"  Pedidos rejeitados: {resultado['nao_alocados']} ✗ (sem capacidade)")
    print(f"  Taxa de sucesso: {(resultado['alocados']/num_pedidos*100):.1f}%")
    
    print(f"\n⏱️  Tempos:")
    print(f"  Tempo para completar: {resultado['tempo_total_minutos']:.1f} minutos")
    print(f"  Tempo médio por pedido: {resultado['tempo_medio_minutos']:.1f} minutos")
    
    print(f"\n📊 Throughput:")
    print(f"  Taxa: {resultado['throughput_pedidos_por_min']:.3f} pedidos/minuto")
    print(f"  Taxa: {resultado['throughput_pedidos_por_min']*60:.1f} pedidos/hora")
    
    print(f"\n⚠️  Gargalo Identificado: {resultado['gargalo']}")
    
    if resultado['gargalo'] == 'Produção':
        print("    💡 Sugestão: Aumentar slots de produção ou reduzir tempo por pedido")
    elif resultado['gargalo'] == 'Entrega':
        print("    💡 Sugestão: Aumentar número de entregadores ou capacidade por viagem")
    else:
        print("    ✓ Sistema bem balanceado!")
    
    input("\nPressione Enter para voltar...")


def infraestrutura_minima(grafo):
    """Calcula a infraestrutura mínima usando Prim MST."""
    limpar_tela()
    print("-" * 60)
    print("INFRAESTRUTURA MÍNIMA (Prim MST)")
    print("-" * 60)
    print("\nQual é o menor custo de conexões para interligar todas as regiões?")
    print("(Aplicável para planejamento de estradas, fibra, etc.)")
    
    # Calcular MST
    infra = InfraestruturaMinima(grafo)
    custo_total, arestas = infra.calcular()
    
    if not arestas:
        print("\n⚠️  Grafo desconexo ou vazio!")
        input("\nPressione Enter para voltar...")
        return
    
    # Exibir resultado
    print(f"\n✓ Árvore Geradora Mínima encontrada:")
    print(f"  Custo total: {custo_total:.1f} unidades")
    print(f"  Número de conexões necessárias: {len(arestas)}")
    print(f"  (Conecta {len(arestas) + 1} regiões)")
    
    print(f"\n📍 Arestas da infraestrutura mínima:")
    for origem, destino, tempo in arestas:
        print(f"  {origem} ↔ {destino}")
        print(f"    Tempo de viagem: {tempo:.1f} minutos")
    
    input("\nPressione Enter para voltar...")
