# receitas por restricao
# sugestao de pratos
# receitas mais bem avaliadas
# Gerar combinações de receitas que atendam a um objetivo específico
#       (ex: menu econômico, menu rápido, etc.)


# Menu por orçamento é guloso pq ao inves de ordenar as receitas
# ele insere no array de receitas do menu a melhor levando em conta
# os candidatos disponíveis quanto ao custo máximo restante
import os


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def comparaReceitas(receita, atual, criterio):
    if atual is None:
        return True

    if receita.avaliacao != atual.avaliacao:
        return receita.avaliacao > atual.avaliacao

    if criterio == 'tempo':
        if receita.tempo != atual.tempo:
            return receita.tempo < atual.tempo
    elif criterio == 'custo':
        if receita.custo != atual.custo:
            return receita.custo < atual.custo
        
    elif criterio == 'dificuldade':
        dificuldade_receita = str(receita.dificuldade or '').lower()
        dificuldade_atual = str(atual.dificuldade or '').lower()
        if dificuldade_receita != dificuldade_atual:
            return dificuldade_receita < dificuldade_atual
    else:
        if receita.custo != atual.custo:
            return receita.custo < atual.custo

    return False

# esse aqui é o que seleciona específicamente
# o comparar é o que compara relacionado ao criterio
def selecionarMelhor(candidatos, criterio):
    melhor = None
    for receita in candidatos:
        if comparaReceitas(receita, melhor, criterio):
            melhor = receita
    return melhor


def cardapioOrcamento(receitas, orcamentoMax):
    menu = []
    custoRestante = orcamentoMax
    candidatos = []
    for r in receitas:
        # Guloso porque só considera o custo e a avaliação, sem pensar em combinações futuras
        if r.custo <= custoRestante:
            candidatos.append(r)

    while True:
        melhor = selecionarMelhor(candidatos, 'custo')
        if melhor is None:
            break
        if melhor.custo > custoRestante:
            break

        menu.append(melhor)
        custoRestante -= melhor.custo
        novosCandidatos = []
        for r in candidatos:
            if r.id != melhor.id and r.custo <= custoRestante:
                novosCandidatos.append(r)
        candidatos = novosCandidatos

    return menu


def sugerirPratosCriterio(receitas, criterio):
    quantidade=5
    sugestoes = []
    candidatos = []
    for r in receitas:
        candidatos.append(r)

    while candidatos and len(sugestoes) < quantidade:
        melhor = selecionarMelhor(candidatos, criterio)
        if melhor is None:
            break
        sugestoes.append(melhor)
        novosCandidatos = []
        for r in candidatos:
            if r.id != melhor.id:
                novosCandidatos.append(r)
        candidatos = novosCandidatos

    return sugestoes


def mochila01(receitas, orcamento_max, valor='avaliacao'):
    # Conversão para centavos
    cap = int(round(float(orcamento_max) * 100))
    n = 0
    pesos = []
    valores = []
    items = []
    for r in receitas:
        peso = int(round(r.custo * 100))
        # valor escalado para inteiro (preserva 2 casas decimais)
        val = int(round((r.avaliacao or 0) * 100))
        pesos.append(peso)
        valores.append(val)
        items.append(r)
        n += 1

    # tabela DP (n+1) x (cap+1)
    dp = []
    for i in range(n + 1):
        row = []
        for _ in range(cap + 1):
            row.append(0)
        dp.append(row)

    for i in range(1, n + 1):
        wi = pesos[i - 1]
        vi = valores[i - 1]
        for w in range(0, cap + 1):
            sem = dp[i - 1][w]
            com = 0
            if wi <= w:
                com = dp[i - 1][w - wi] + vi
            if com > sem:
                dp[i][w] = com
            else:
                dp[i][w] = sem

    # reconstruir solução
    w = cap
    escolhidos = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            escolhidos.append(items[i - 1])
            w -= pesos[i - 1]

    # inverter para ordem original
    selecionados = []
    for i in range(len(escolhidos) - 1, -1, -1):
        selecionados.append(escolhidos[i])

    total_valor = 0.0
    total_custo = 0.0
    for r in selecionados:
        total_valor += (r.avaliacao or 0)
        total_custo += r.custo

    return selecionados, total_valor, total_custo


def modoChef(buscadorMod23):
    receitas = list(buscadorMod23.receitas_originais.values())

    while True:
        limpar_tela()
        print('=' * 40)
        print('          MODO CHEF - GULOSO          ')
        print('=' * 40)
        print('1. Cardápio econômico por orçamento')
        print('2. Sugestões de pratos por critério')
        print('0. Voltar')

        opcao = input('\nEscolha uma opção: ').strip()

        if opcao == '1':
                
            orcamento = input('Digite o orçamento máximo: ').strip()

            menu = cardapioOrcamento(receitas, orcamento)
            if not menu:
                print('Nenhuma receita cabe no orçamento')
            else:
                print('\nCardápio para o orçamento:')
                for receita in menu:
                    print(f"- {receita.nome} | ID: {receita.id} | R$ {receita.custo:.2f}")
                print(f'Orcamento: {orcamento:.2f}')

            input('\nPressione Enter para voltar...')

        elif opcao == '2':
            print('\nCritérios disponíveis:')
            print('1. avaliação')
            print('2. tempo')
            print('3. custo')
            print('4. dificuldade')
            escolha = input('Escolha um critério: ').strip()
            if escolha == '1':
                criterio = 'avaliacao'
            elif escolha == '2':
                criterio = 'tempo'
            elif escolha == '3':
                criterio = 'custo'
            elif escolha == '4':
                criterio = 'dificuldade'
            else:
                print('Critério inválido.')
                input('\nPressione Enter para voltar...')
                continue

            sugestoes = sugerirPratosCriterio(receitas, criterio)
            if not sugestoes:
                print('Nenhuma sugestão disponível.')
            else:
                print(f"\nMelhores sugestões por critério '{criterio}':")
                for receita in sugestoes:
                    print(f"- {receita.nome} | ID: {receita.id} | R$ {receita.custo:.2f} | Avaliação: {receita.avaliacao}")

            input('\nPressione Enter para voltar...')

        elif opcao == '0':
            break
        else:
            print('Opção inválida!')
            input('\nPressione Enter para voltar...')


