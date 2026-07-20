"""
MÓDULO 7 - JUSTIFICATIVAS TÉCNICAS

============================================================================
1. ESTRUTURAS DE DADOS
============================================================================

classe Regiao:
  ├─ Por que? Modelo simples e natural de "lugar geográfico"
  ├─ O que? Um ponto no mapa com ID, nome, coordenadas (x, y)
  └─ Uso: Centro das entregas, onde chegam os pedidos

classe Cozinha(regiao_id):
  ├─ Por que? Precisa modelar CAPACIDADE e LOCALIZAÇÃO
  ├─ Atributos cruciais:
  │  ├─ slots_producao: quantos pedidos prepara simultaneamente
  │  ├─ tempo_por_pedido: quanto tempo leva preparar um
  │  └─ regiao_id: onde está localizada (em qual Regiao)
  ├─ Raciocínio: Capacidade determina GARGALO DE PRODUÇÃO
  └─ Exemplo: Cozinha central com 3 slots, 5 min/pedido
             = máximo 36 pedidos/hora = 0.6 pedidos/min

classe Entregador:
  ├─ Por que? Precisa modelar CAPACIDADE DE ENTREGA
  ├─ Atributos cruciais:
  │  ├─ capacidade: quantos pedidos carrega por vez
  │  ├─ velocidade_kmh: afeta tempo de viagem
  │  └─ regiao_atual: onde está (para routing)
  ├─ Raciocínio: Capacidade determina GARGALO DE ENTREGA
  └─ Exemplo: 3 entregadores × 2 pedidos = 6 pedidos simultâneos

classe Pedido:
  ├─ Por que? Unidade básica de trabalho que flui pela rede
  ├─ Atributos:
  │  ├─ regiao_destino: para onde vai
  │  ├─ tempo_preparo: quando sai da cozinha
  │  └─ prioridade: urgentes vão primeiro (equidade)
  └─ Raciocínio: Permite rastrear fluxo e fazer alocações

classe Aresta:
  ├─ Por que? Representa "rota entre dois pontos"
  ├─ Atributos:
  │  ├─ tempo_minutos: tempo de viagem
  │  ├─ custo: custo operacional (combustível, manutenção)
  │  └─ capacidade: quantos pedidos simultâneos nesta rota
  └─ Uso: Dijkstra usa tempo_minutos, Prim usa custo


============================================================================
2. GRAFO LOGÍSTICO
============================================================================

Por que usar GRAFO?
  • Estrutura natural para modelar REDE DE DISTRIBUIÇÃO
  • Nós = pontos (regiões, cozinhas, pontos de retirada)
  • Arestas = rotas possíveis entre pontos
  • Permite algoritmos clássicos (Dijkstra, Prim, BFS, etc)

Estrutura interna:
  adjacencia = {
    'rgn_centro': [
      ('rgn_norte', Aresta(...)),
      ('rgn_sul', Aresta(...))
    ],
    'rgn_norte': [
      ('rgn_centro', Aresta(...))
    ],
    ...
  }

Por que dict + list (e não objeto Graph complexo)?
  • Simplicidade: sem dependências externas
  • Clareza: fácil de entender e debugar
  • Flexibilidade: pode adicionar dados onde quiser


============================================================================
3. ALGORITMO: DIJKSTRA (Roteamento)
============================================================================

O PROBLEMA:
  "Qual a rota mais rápida de A até B?"
  "Quantos minutos leva?"

POR QUE DIJKSTRA?
  ✓ Encontra o caminho MAIS CURTO (em tempo)
  ✓ Algoritmo clássico, bem estudado
  ✓ Complexidade O(V²) é aceitável (V < 100 regiões)
  ✓ Funciona em grafos com pesos positivos (nosso caso)

COMO FUNCIONA (simplificado):
  1. Marcar distâncias: origem=0, outros=∞
  2. Repetir V vezes:
     a) Escolher nó não visitado mais próximo
     b) Para cada vizinho:
        - Se encontrar caminho mais curto, atualizar
  3. Resultado: tabela de distâncias mínimas

COMPLEXIDADE:
  • Tempo: O(V²) - V iterações, cada uma percorre V nós
  • Espaço: O(V) - armazena distâncias
  • Aceitável para V < 100

EXEMPLO:
  Centro (0 min)
    ├→ Norte (15 min)
    ├→ Sul (15 min)
    └→ Leste (20 min = 10 Centro-Sul + 10 Sul-Leste)

RETORNA:
  • tempo_total: 15.0 minutos
  • caminho: ['rgn_centro', 'rgn_norte']


============================================================================
4. ALGORITMO: PRIM MST (Infraestrutura Mínima)
============================================================================

O PROBLEMA:
  "Precisamos conectar 4 cidades. Qual é o menor custo?"
  "Que ruas (arestas) são imprescindíveis?"

POR QUE PRIM?
  ✓ Encontra Árvore Geradora Mínima (MST)
  ✓ Garante que TODOS os nós ficam conectados
  ✓ Com MENOR CUSTO TOTAL
  ✓ Complexidade O(E²) aceitável para nossa escala

COMO FUNCIONA:
  1. Começar com nó qualquer (ex: centro)
  2. Repetir (V-1) vezes:
     a) Encontrar aresta de menor custo que sai da árvore
     b) Adicionar essa aresta e novo nó
  3. Resultado: V-1 arestas formando árvore conectada

EXEMPLO (4 cidades):
  Arestas originais:
    Centro-Norte: 50
    Centro-Sul: 50
    Centro-Leste: 60
    Norte-Leste: 70
    Sul-Leste: 80

  Prim MST resultado:
    Centro-Norte: 50 ✓
    Centro-Sul: 50 ✓
    Centro-Leste: 60 ✓
    Total: 160 (sem Norte-Leste e Sul-Leste)

COMPLEXIDADE:
  • Tempo: O(E²) - V rodadas, cada uma verifica até E arestas
  • Espaço: O(V + E) - armazena grafo
  • Aceitável para E < 1000


============================================================================
5. ALGORITMO: ALOCADOR GULOSO (Distribuição de Pedidos)
============================================================================

O PROBLEMA:
  "Temos 10 pedidos, 2 cozinhas e 3 entregadores"
  "Como distribuir de forma eficiente?"

POR QUE GULOSO (greedy)?
  ✓ Decisão ótima LOCAL em cada passo
  ✓ Rápido: O(P × C × E) onde P=pedidos, C=cozinhas, E=entregadores
  ✓ Adequado para decisões em tempo real (sem otimização exata)
  ✓ Simples de implementar e entender

COMO FUNCIONA:
  1. Ordenar pedidos: URGENTES PRIMEIRO, depois por tempo
  2. Para cada pedido (por ordem):
     a) Escolher cozinha com MENOR OCUPAÇÃO
     b) Escolher entregador com MENOR CARGA
     c) Se ambos têm capacidade, alocar
     d) Senão, marcar como "não alocado"

EXEMPLO (passo a passo):
  Cozinhas: Cz_A (3 slots), Cz_B (2 slots) - ambas vazias
  Entregadores: Entr1 (cap 2), Entr2 (cap 2), Entr3 (cap 2)

  Pedido 1: → Cz_A (vazia), Entr1 (vazia)     ✓ Alocado
  Pedido 2: → Cz_A (1/3), Entr2 (vazia)       ✓ Alocado
  Pedido 3: → Cz_A (2/3), Entr3 (vazia)       ✓ Alocado
  Pedido 4: → Cz_A (3/3 CHEIO!), ...          ✗ Tenta Cz_B
            → Cz_B (vazia), Entr1 (1/2)       ✓ Alocado
  Pedido 5: → Cz_B (1/2), Entr2 (1/2)         ✓ Alocado
  Pedido 6: → Cz_B (2/2 CHEIO!), ...          ✗ Sem capacidade

COMPLEXIDADE:
  • Tempo: O(P × log(C)) se usar min(), O(P × C) versão simples
  • Espaço: O(P)
  • Instantâneo para decisões em tempo real

LIMITAÇÃO:
  ✓ Não garante ÓTIMO GLOBAL (mas é rápido)
  ✗ Pedidos anteriores podem bloquear posteriores
  → Solução: Usar ordenação por prioridade


============================================================================
6. SIMULADOR DE CAPACIDADE (Análise de Gargalos)
============================================================================

O PROBLEMA:
  "Quantos pedidos conseguimos atender?"
  "Qual é o gargalo do sistema?"

RACIOCÍNIO:
  Capacidade total = min(capacidade_producao, capacidade_entrega)
  
  Se:
    Producao < Entrega → GARGALO EM PRODUÇÃO (cozinhas lentas)
    Entrega < Producao → GARGALO EM ENTREGA (poucos entregadores)
    Producao = Entrega → BALANCEADO

COMO CALCULA:

  1. Capacidade de Produção (pedidos/minuto):
     = (total_slots_producao × 60) / tempo_por_pedido
     
     Exemplo:
       Cz_A: 3 slots, 5 min → (3 × 60) / 5 = 36 pedidos/hora = 0.6/min
       Cz_B: 2 slots, 6 min → (2 × 60) / 6 = 20 pedidos/hora = 0.33/min
       Total: 0.93 pedidos/minuto

  2. Capacidade de Entrega (pedidos/minuto):
     = (num_entregadores × capacidade_cada_um) / tempo_medio_viagem
     
     Exemplo:
       3 entregadores × 2 pedidos = 6 simultâneos
       Tempo médio viagem = 10 minutos
       Throughput: 6 / 10 = 0.6 pedidos/minuto

  3. Gargalo = min(0.93, 0.6) = ENTREGA é o gargalo!

SIMULAÇÃO DE PICO:
  1. Criar N pedidos simultâneos
  2. Alocar cada um (marca ocupação)
  3. Calcular tempo conclusão = preparo + entrega
  4. Throughput = pedidos_alocados / tempo_total

RETORNA:
  • alocados: quantos pedidos conseguiram ser alocados
  • nao_alocados: quantos não couberam
  • tempo_total_minutos: quando último pedido é entregue
  • throughput_pedidos_por_min: taxa de conclusão
  • gargalo: "Produção" ou "Entrega"


============================================================================
7. RESPOSTAS AOS 4 PROBLEMAS PROPOSTOS
============================================================================

Problema 1: "Quantos pedidos podem ser atendidos simultaneamente?"
  Resposta: SimuladorCapacidade.simular_pico(pedidos)
  Retorna: alocados = 5 (limitado por cozinhas ou entregadores)

Problema 2: "Como distribuir pedidos entre entregadores?"
  Resposta: AlocadorGuloso.alocar(pedidos)
  Heurística: pedido → cozinha_menos_ocupada + entregador_menos_carregado
  Resultado: {pedido_id → (cozinha_id, entregador_id)}

Problema 3: "Qual a capacidade máxima de atendimento?"
  Resposta: SimuladorCapacidade.estimar_throughput_maximo()
  Cálculo: min(cap_producao, cap_entrega)
  Resultado: 0.6 pedidos/minuto = 36 pedidos/hora

Problema 4: "Existe gargalo operacional?"
  Resposta: Comparar capacidades em simular_pico()
  Se cap_producao < cap_entrega → gargalo em PRODUÇÃO
  Se cap_entrega < cap_producao → gargalo em ENTREGA


============================================================================
8. DESACOPLAMENTO PARA INTEGRAÇÃO COM MAIN.PY
============================================================================

Estrutura proposta para main.py:

1. INICIALIZAÇÃO:
   from exemplo_modulo7 import criar_sistema_logistica_exemplo
   
   grafo, cozinhas, entregadores, regioes = criar_sistema_logistica_exemplo()

2. MENU PRINCIPAL:
   Um dos itens: "Módulo 7 - Logística"
   
   Este abre submenu:
   ├─ 1. Consultar rotas
   ├─ 2. Alocação de pedidos
   ├─ 3. Análise de capacidade
   ├─ 4. Simulação de pico
   └─ 5. Infraestrutura mínima

3. CADA SUBMENU:
   ├─ Recebe grafo, cozinhas, entregadores
   ├─ Executa operação (Dijkstra, Prim, etc)
   ├─ Exibe resultado
   └─ Volta ao menu

4. VANTAGENS:
   ✓ Módulo 7 não conhece main.py (desacoplado)
   ✓ Main.py importa e chama funções do módulo 7
   ✓ Fácil testar separadamente
   ✓ Fácil estender posteriormente


============================================================================
9. EXEMPLO DE INTEGRAÇÃO NO MAIN.PY
============================================================================

# No início do main.py:
from exemplo_modulo7 import criar_sistema_logistica_exemplo

# Função para inicializar tudo:
def inicializar_sistema():
    global grafo, cozinhas, entregadores, regioes
    grafo, cozinhas, entregadores, regioes = criar_sistema_logistica_exemplo()

# No menu principal, adicionar opção:
def menu_principal():
    while True:
        print("1. Receitas")
        print("2. Investigação")
        print("3. Chef")
        print("4. Módulo 7 - Logística")  # ← AQUI!
        print("5. Sair")
        
        opcao = input("Escolha: ")
        
        if opcao == "4":
            menu_logistica(grafo, cozinhas, entregadores)

# Novo menu para logística:
def menu_logistica(grafo, cozinhas, entregadores):
    from modulos.modulo7 import RoteadorDijkstra, AlocadorGuloso, SimuladorCapacidade
    
    while True:
        print("\n=== MÓDULO 7 - LOGÍSTICA ===")
        print("1. Consultar rota")
        print("2. Alocar pedidos")
        print("3. Analisar capacidade")
        print("4. Simular pico")
        print("5. Voltar")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            roteador = RoteadorDijkstra(grafo)
            origem = input("Origem: ")
            destino = input("Destino: ")
            tempo, caminho = roteador.caminho_mais_curto(origem, destino)
            print(f"Rota: {' → '.join(caminho)} ({tempo:.1f} min)")
        
        # ... mais opções ...
        
        elif opcao == "5":
            break


============================================================================
10. JUSTIFICATIVA FINAL
============================================================================

Por que escolher estas estruturas e algoritmos?

✓ SIMPLICIDADE: Código limpo, sem bibliotecas externas
✓ EFICIÊNCIA: O(V²) e O(E²) é aceitável para cenários reais
✓ FUNCIONALIDADE: Responde todas as 4 perguntas do requisito
✓ DESACOPLAMENTO: Pronto para integrar com qualquer interface
✓ EXTENSIBILIDADE: Fácil adicionar novos algoritmos depois
  
Alternativas descartadas:
✗ Min-heap (heapq): Precisa de import externo
✗ Dataclasses: Precisa de import externo
✗ Grafos complexos (networkx): Overhead desnecessário
✗ BD relacional: Overkill para este escopo

Conclusão:
Implementação enxuta, robusta e educacional que ensina
conceitos fundamentais de grafos e algoritmos.
"""
