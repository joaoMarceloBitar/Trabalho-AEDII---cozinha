"""
MÓDULO 7 — O PESADELO LOGÍSTICO
Modelagem de rede de distribuição para serviço de delivery

CONCEITOS PRINCIPAIS:
1. Grafo de regiões: conecta cozinhas e pontos de retirada
2. Dijkstra: encontra rotas mais rápidas entre pontos
3. Prim MST: determina infraestrutura mínima de conexões
4. Alocador guloso: distribui pedidos aos recursos disponíveis
5. Simulador: estima capacidade máxima do sistema
"""


# ============================================================================
# PARTE 1: ESTRUTURAS DE DADOS
# ============================================================================

class Regiao:
    """
    Representa um ponto geográfico na rede.
    JUSTIFICATIVA: Modelo simples de localização com nome e ID.
    Atributos:
        id: Identificador único
        nome: Descrição legível
        x, y: Coordenadas para cálculo de distâncias
        pedidos_em_fila: Quantos pedidos aguardam nesta região
    """
    def __init__(self, id, nome, x, y):
        self.id = id
        self.nome = nome
        self.x = x
        self.y = y
        self.pedidos_em_fila = 0


class Cozinha:
    """
    Estação de preparo localizada em uma região.
    JUSTIFICATIVA: Necessária para modelar capacidade de produção.
    Atributos:
        id: Identificador único
        nome: Descrição
        regiao_id: Qual região está localizada
        slots_producao: Quantos pedidos prepara simultaneamente
        tempo_por_pedido: Minutos para preparar um pedido
    """
    def __init__(self, id, nome, regiao_id, slots_producao, tempo_por_pedido):
        self.id = id
        self.nome = nome
        self.regiao_id = regiao_id
        self.slots_producao = slots_producao
        self.tempo_por_pedido = tempo_por_pedido
        self.pedidos_em_preparacao = 0  # Contador de ocupação


class Entregador:
    """
    Recurso responsável por entregas.
    JUSTIFICATIVA: Necessária para modelar restrição de capacidade de entrega.
    Atributos:
        id: Identificador único
        nome: Descrição
        velocidade_kmh: Velocidade média em km/h
        capacidade: Quantos pedidos carrega por vez
        regiao_atual: Onde está localizado
    """
    def __init__(self, id, nome, velocidade_kmh, capacidade, regiao_atual):
        self.id = id
        self.nome = nome
        self.velocidade_kmh = velocidade_kmh
        self.capacidade = capacidade
        self.regiao_atual = regiao_atual
        self.pedidos_que_carrega = 0  # Contador de ocupação


class Pedido:
    """
    Representa uma solicitação de entrega.
    JUSTIFICATIVA: Necessária para rastrear o fluxo de pedidos na rede.
    Atributos:
        id: Identificador único
        regiao_destino: Onde será entregue
        tempo_preparo: Quanto tempo leva para preparar (da receita)
        prioridade: 0=normal, 1=urgente (para simulação)
    """
    def __init__(self, id, regiao_destino, tempo_preparo, prioridade=0):
        self.id = id
        self.regiao_destino = regiao_destino
        self.tempo_preparo = tempo_preparo
        self.prioridade = prioridade
        self.tempo_criacao = 0  # Será preenchido pela simulação


class Aresta:
    """
    Representa uma conexão entre duas regiões.
    JUSTIFICATIVA: Modelo simples para dados da aresta (custo, tempo).
    Atributos:
        origem: ID da região de saída
        destino: ID da região de chegada
        tempo_minutos: Tempo de viagem entre regiões
        custo: Custo de operação desta rota
        capacidade: Quantos pedidos simultaneamente (máx 1 por viagem tipicamente)
    """
    def __init__(self, origem, destino, tempo_minutos, custo, capacidade=1):
        self.origem = origem
        self.destino = destino
        self.tempo_minutos = tempo_minutos
        self.custo = custo
        self.capacidade = capacidade


# ============================================================================
# PARTE 2: GRAFO LOGÍSTICO
# ============================================================================

class GrafoLogistico:
    """
    Representa a rede de regiões, cozinhas e entregas.
    
    JUSTIFICATIVA DA ESTRUTURA:
    - Grafo é a forma natural de modelar uma rede logística
    - Nós = regiões, cozinhas, pontos de retirada
    - Arestas = rotas possíveis com tempos de viagem
    - Permite algoritmos de caminho mais curto (Dijkstra)
    - Permite calcular infraestrutura mínima (Prim MST)
    
    ESTRUTURA INTERNA:
    - adjacencia: dicionário {id_origem: [(id_destino, Aresta), ...]}
    - nos: dicionário {id: Regiao/Cozinha/etc}
    """
    
    def __init__(self):
        self.nos = {}  # id -> objeto (Regiao, Cozinha, etc)
        self.adjacencia = {}  # id -> lista de (vizinho_id, Aresta)
    
    def adicionar_no(self, no):
        """Adiciona uma região, cozinha ou ponto de retirada ao grafo."""
        self.nos[no.id] = no
        if no.id not in self.adjacencia:
            self.adjacencia[no.id] = []
    
    def adicionar_aresta(self, origem_id, destino_id, tempo, custo, bidirecional=True):
        """
        Adiciona uma rota entre dois pontos.
        Se bidirecional=True, cria duas arestas (ida e volta).
        """
        aresta = Aresta(origem_id, destino_id, tempo, custo)
        self.adjacencia[origem_id].append((destino_id, aresta))
        
        if bidirecional:
            aresta_volta = Aresta(destino_id, origem_id, tempo, custo)
            self.adjacencia[destino_id].append((origem_id, aresta_volta))
    
    def vizinhos(self, id_no):
        """Retorna lista de vizinhos de um nó."""
        return self.adjacencia.get(id_no, [])


# ============================================================================
# PARTE 3: ALGORITMOS DE ROTEAMENTO
# ============================================================================

class RoteadorDijkstra:
    """
    Implementa algoritmo de Dijkstra para encontrar caminho mais rápido.
    
    JUSTIFICATIVA:
    - Dijkstra encontra caminho MAIS RÁPIDO entre dois pontos
    - Necessário para responder: "qual é a rota mais eficiente?"
    - Complexidade O(V²) é aceitável para V < 100 (nossas regiões)
    - Sem necessidade de lib externa (heap)
    
    ALGORITMO (simplificado):
    1. Marcar todas as distâncias como infinito
    2. Distância da origem = 0
    3. Enquanto há nós não visitados:
        a) Pegar nó não visitado mais próximo
        b) Para cada vizinho:
            - Se encontrar caminho mais curto, atualizar
    4) Retornar: distâncias mínimas e anterior de cada nó (para reconstruir caminho)
    """
    
    def __init__(self, grafo):
        self.grafo = grafo
    
    def calcular(self, origem_id):
        """
        Calcula distâncias mínimas de 'origem_id' para todos os nós.
        Retorna:
            distancias: {id_destino: tempo_minimo}
            anterior: {id_destino: id_anterior} para reconstruir caminho
        """
        distancias = {no_id: float('inf') for no_id in self.grafo.nos}
        anterior = {no_id: None for no_id in self.grafo.nos}
        visitados = set()
        
        distancias[origem_id] = 0
        
        # Iterador V vezes (uma para cada nó)
        for _ in range(len(self.grafo.nos)):
            # Encontrar nó não visitado com menor distância
            min_no = None
            min_distancia = float('inf')
            
            for no_id in self.grafo.nos:
                if no_id not in visitados and distancias[no_id] < min_distancia:
                    min_no = no_id
                    min_distancia = distancias[no_id]
            
            if min_no is None or min_distancia == float('inf'):
                break
            
            visitados.add(min_no)
            
            # Relaxar arestas saindo de min_no
            for vizinho_id, aresta in self.grafo.vizinhos(min_no):
                novo_custo = distancias[min_no] + aresta.tempo_minutos
                
                if novo_custo < distancias[vizinho_id]:
                    distancias[vizinho_id] = novo_custo
                    anterior[vizinho_id] = min_no
        
        return distancias, anterior
    
    def caminho_mais_curto(self, origem_id, destino_id):
        """
        Retorna: (tempo_total, lista_de_nos_no_caminho)
        Exemplo: (15.0, ['cz_principal', 'rgn_norte'])
        """
        distancias, anterior = self.calcular(origem_id)
        
        if distancias[destino_id] == float('inf'):
            return None, []  # Sem caminho possível
        
        # Reconstruir caminho pelo anterior
        caminho = []
        no_atual = destino_id
        while no_atual is not None:
            caminho.append(no_atual)
            no_atual = anterior[no_atual]
        caminho.reverse()
        
        return distancias[destino_id], caminho


# ============================================================================
# PARTE 4: INFRAESTRUTURA MÍNIMA (PRIM MST)
# ============================================================================

class InfraestruturaMinima:
    """
    Implementa algoritmo de Prim para encontrar Árvore Geradora Mínima.
    
    JUSTIFICATIVA:
    - Problema: "deseja-se determinar a menor rede de conexões"
    - Prim MST encontra conjunto mínimo de arestas que conecta TODOS os nós
    - Objetivo: reduzir custos de infraestrutura mantendo rede conectada
    - Complexidade O(E²) sem heap (aceitável para nossa escala)
    
    ALGORITMO (simplificado):
    1) Começar com um nó qualquer na árvore
    2) Repetir V-1 vezes:
        a) Encontrar aresta de menor custo que conecta árvore a fora da árvore
        b) Adicionar essa aresta e novo nó à árvore
    3) Resultado: V-1 arestas formando árvore conectada com custo mínimo
    """
    
    def __init__(self, grafo):
        self.grafo = grafo
    
    def calcular(self):
        """
        Calcula MST.
        Retorna:
            custo_total: soma dos custos das arestas
            arestas_agm: lista de (origem, destino, tempo) da árvore
        """
        if not self.grafo.nos:
            return 0, []
        
        # Começar com primeiro nó
        nos_lista = list(self.grafo.nos.keys())
        na_arvore = {nos_lista[0]}
        arestas_agm = []
        custo_total = 0
        
        # Adicionar V-1 arestas
        while len(na_arvore) < len(self.grafo.nos):
            # Encontrar aresta de menor custo: árvore -> fora
            melhor_aresta = None
            melhor_custo = float('inf')
            
            for no_id in na_arvore:
                for vizinho_id, aresta in self.grafo.vizinhos(no_id):
                    if vizinho_id not in na_arvore:
                        if aresta.custo < melhor_custo:
                            melhor_aresta = (no_id, vizinho_id, aresta)
                            melhor_custo = aresta.custo
            
            if melhor_aresta is None:
                break  # Grafo desconexo
            
            origem, destino, aresta = melhor_aresta
            na_arvore.add(destino)
            arestas_agm.append((origem, destino, aresta.tempo_minutos))
            custo_total += aresta.custo
        
        return custo_total, arestas_agm


# ============================================================================
# PARTE 5: ALOCADOR DE PEDIDOS
# ============================================================================

class AlocadorGuloso:
    """
    Distribui pedidos entre cozinhas e entregadores.
    
    JUSTIFICATIVA:
    - Algoritmo guloso escolhe melhor opção local a cada passo
    - Complexidade O(pedidos × cozinhas × entregadores)
    - Suficiente para decisões em tempo real (sem otimização global)
    - Objetivo: responder "como distribuir pedidos?"
    
    ESTRATÉGIA:
    1. Ordenar pedidos por prioridade (urgentes primeiro)
    2. Para cada pedido:
        a) Encontrar cozinha com menos ocupação
        b) Encontrar entregador com menos carga
        c) Alocar se houver capacidade
    """
    
    def __init__(self, grafo, cozinhas, entregadores):
        self.grafo = grafo
        self.cozinhas = cozinhas  # lista
        self.entregadores = entregadores  # lista
        self.roteador = RoteadorDijkstra(grafo)
    
    def alocar(self, pedidos):
        """
        Aloca pedidos a cozinhas e entregadores.
        Retorna:
            alocacoes: {pedido_id: (cozinha_id, entregador_id)}
            nao_alocados: lista de pedidos que não couberam
        """
        # Ordenar pedidos: urgentes primeiro, depois por tempo criação
        pedidos_ordenados = sorted(
            pedidos,
            key=lambda p: (-p.prioridade, p.tempo_criacao)
        )
        
        alocacoes = {}
        nao_alocados = []
        
        for pedido in pedidos_ordenados:
            # Encontrar cozinha com menor ocupação
            cozinha = min(self.cozinhas, key=lambda c: c.pedidos_em_preparacao)
            
            # Verificar capacidade
            if cozinha.pedidos_em_preparacao >= cozinha.slots_producao:
                nao_alocados.append(pedido)
                continue
            
            # Encontrar entregador com menor carga
            entregador = min(self.entregadores, key=lambda e: e.pedidos_que_carrega)
            
            # Verificar capacidade
            if entregador.pedidos_que_carrega >= entregador.capacidade:
                nao_alocados.append(pedido)
                continue
            
            # ALOCAR
            cozinha.pedidos_em_preparacao += 1
            entregador.pedidos_que_carrega += 1
            alocacoes[pedido.id] = (cozinha.id, entregador.id)
        
        return alocacoes, nao_alocados


# ============================================================================
# PARTE 6: SIMULADOR DE CAPACIDADE
# ============================================================================

class SimuladorCapacidade:
    """
    Estima capacidade máxima de atendimento considerando restrições.
    
    JUSTIFICATIVA:
    - Simula cenário de pico com várias requisições simultâneas
    - Rastreia tempos de preparo + entrega para cada pedido
    - Identifica gargalo: que recurso (cozinha vs entrega) é o limitante?
    - Responde: "qual capacidade máxima?", "existe gargalo?"
    
    LÓGICA:
    1. Criar N pedidos em sequência rápida
    2. Alocar cada um (marca tempo ocupação)
    3. Simular conclusão: max(tempo_preparo, tempo_entrega)
    4. Calcular throughput: pedidos/tempo_total
    5. Comparar: cap_producao vs cap_entrega para detectar gargalo
    """
    
    def __init__(self, alocador, cozinhas, entregadores, grafo):
        self.alocador = alocador
        self.cozinhas = cozinhas
        self.entregadores = entregadores
        self.grafo = grafo
        self.roteador = RoteadorDijkstra(grafo)
    
    def estimar_throughput_maximo(self, tempo_simular_minutos):
        """
        Estima quantos pedidos por minuto o sistema consegue processar.
        Retorna: pedidos_por_minuto (float)
        """
        if not self.cozinhas or not self.entregadores:
            return 0
        
        cozinha = self.cozinhas[0]
        
        # Capacidade de produção: slots × (60 / tempo_por_pedido)
        pedidos_hora_cozinha = (cozinha.slots_producao * 60) / cozinha.tempo_por_pedido
        
        # Capacidade de entrega: entregadores × capacidade × turnos/hora
        # (simplificação: assume 1 entrega = 10 min de viagem média)
        pedidos_hora_entrega = (
            len(self.entregadores) * self.entregadores[0].capacidade * 6
        )
        
        # Gargalo: o menor dos dois
        throughput_maximo = min(pedidos_hora_cozinha, pedidos_hora_entrega)
        
        return throughput_maximo / 60  # Converter para por minuto
    
    def simular_pico(self, pedidos):
        """
        Simula alocação de múltiplos pedidos em pico.
        Retorna: dict com métricas
            {
                'alocados': int,
                'nao_alocados': int,
                'tempo_medio_minutos': float,
                'throughput_pedidos_por_min': float,
                'gargalo': str (cozinha ou entrega)
            }
        """
        # Zerar contadores
        for c in self.cozinhas:
            c.pedidos_em_preparacao = 0
        for e in self.entregadores:
            e.pedidos_que_carrega = 0
        
        # Definir tempo de criação para cada pedido
        tempo_agora = 0
        for i, pedido in enumerate(pedidos):
            pedido.tempo_criacao = tempo_agora
        
        # Alocar
        alocacoes, nao_alocados = self.alocador.alocar(pedidos)
        
        # Simular tempos
        tempos_conclusao = []
        for pedido in pedidos:
            if pedido.id in alocacoes:
                # Tempo total = preparo + entrega
                tempo_conclusao = pedido.tempo_preparo + 10  # 10 min viagem média
                tempos_conclusao.append(tempo_conclusao)
        
        tempo_total = max(tempos_conclusao) if tempos_conclusao else 0
        tempo_medio = sum(tempos_conclusao) / len(tempos_conclusao) if tempos_conclusao else 0
        
        # Calcular throughput
        alocados = len(alocacoes)
        throughput = alocados / tempo_total if tempo_total > 0 else 0
        
        # Detectar gargalo
        cap_producao = (
            sum(c.slots_producao for c in self.cozinhas) * 60 / 
            (self.cozinhas[0].tempo_por_pedido if self.cozinhas else 1)
        ) / 60
        cap_entrega = len(self.entregadores) * self.entregadores[0].capacidade / 10 if self.entregadores else 0
        
        if cap_producao < cap_entrega:
            gargalo = "Produção"
        elif cap_entrega < cap_producao:
            gargalo = "Entrega"
        else:
            gargalo = "Balanceado"
        
        return {
            'alocados': alocados,
            'nao_alocados': len(nao_alocados),
            'tempo_medio_minutos': tempo_medio,
            'tempo_total_minutos': tempo_total,
            'throughput_pedidos_por_min': throughput,
            'gargalo': gargalo
        }
