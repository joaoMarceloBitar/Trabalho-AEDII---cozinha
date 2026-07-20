# receitas por restricao
# sugestao de pratos
# receitas mais bem avaliadas
# Gerar combinações de receitas que atendam a um objetivo específico
#       (ex: menu econômico, menu rápido, etc.)


# Menu por orçamento é guloso pq ao inves de ordenar as receitas
# ele insere no array de receitas do menu a melhor levando em conta
# os candidatos disponíveis quanto ao custo máximo restante
import os

from modulos.modulo5 import sequencia_producao_menu
from modulos import modulo6


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


def sequenciaProducaoMenuDoDia(grafoDependencias, infoDependencias, buscadorMod23):
    print('\nDigite os IDs das receitas do menu do dia, separados por vírgula:')
    entrada = input('IDs: ').strip()
    idsAlvo = [idReceita.strip() for idReceita in entrada.split(',') if idReceita.strip()]

    if not idsAlvo:
        print('\nNenhum ID informado.')
        return

    resultado = sequencia_producao_menu(grafoDependencias, infoDependencias, buscadorMod23, idsAlvo)

    if not resultado.sucesso:
        print(f'\n{resultado.mensagem_erro}')
        return

    print('\nSequência correta de produção para o menu do dia:')
    for indice, nome in enumerate(resultado.ordem, start=1):
        print(f'  {indice}. {nome}')



# Módulo 6 - Menu Degustação VIP (Otimização por Mochila 0/1)


def _lerFloatPositivo(mensagem):
    #Lê um número positivo; devolve None se a entrada for inválida/vazia.
    entrada = input(mensagem).strip().replace(',', '.')
    if not entrada:
        return None
    try:
        valor = float(entrada)
    except ValueError:
        print('Valor inválido.')
        return None
    if valor <= 0:
        print('O valor deve ser positivo.')
        return None
    return valor


def _lerRestricoesOpcionais(receitas):
    #Coleta os filtros duros opcionais do Módulo 6. Enter em branco = pular.
    disponiveis = None
    entrada = input('\nIngredientes disponíveis em estoque (separados por vírgula, Enter p/ ignorar): ').strip()
    if entrada:
        disponiveis = {i.strip().lower() for i in entrada.split(',') if i.strip()}

    max_raros = None
    entrada = input('Limite de ingredientes RAROS por prato (Enter p/ ignorar): ').strip()
    if entrada:
        try:
            max_raros = int(entrada)
            if max_raros < 0:
                print('Limite negativo ignorado.')
                max_raros = None
        except ValueError:
            print('Limite inválido ignorado.')

    dificuldades = None
    resposta = input('A equipe consegue produzir pratos DIFÍCEIS hoje? (s/N): ').strip().lower()
    if resposta != 's':
        # Capacidade da equipe reduzida: bloqueia os "Difícil".
        dificuldades = {'fácil', 'média'}

    return disponiveis, max_raros, dificuldades


def _escolherCriterio():
    #Submenu de critério de otimização. Devolve (chave, rótulo) ou (None, None).
    print('\nCritério de otimização:')
    print('1. Maior lucro')
    print('2. Melhor avaliação (soma; reporta a média)')
    print('3. Maior popularidade')
    escolha = input('Escolha um critério: ').strip()
    return {
        '1': ('lucro', 'lucro'),
        '2': ('avaliacao', 'avaliação'),
        '3': ('popularidade', 'popularidade'),
    }.get(escolha, (None, None))


def _exibirMenuOtimizado(resultado, criterio, criterioLabel, orcamento, tempoMax):
    #Formata o resultado do Módulo 6: pratos, valor do critério, consumo e justificativa.
    if not resultado.sucesso:
        print(f'\n{resultado.mensagem_erro}')
        return

    receitas = resultado.receitas
    custoTotal = sum(r.custo for r in receitas)
    tempoTotal = sum(r.tempo for r in receitas)
    mediaAval = sum(r.avaliacao for r in receitas) / len(receitas)

    print('\n' + '=' * 55)
    print('        MENU DEGUSTAÇÃO VIP - SUGESTÃO OTIMIZADA')
    print('=' * 55)
    print(f'Candidatas consideradas após filtros: {resultado.candidatos_considerados}')
    print(f'Pratos escolhidos: {len(receitas)}\n')
    for r in receitas:
        print(f'  - {r.nome[:35]:<35} | R$ {r.custo:6.2f} | {r.tempo:>3}min | aval {r.avaliacao:.1f} | {r.dificuldade}')

    print('\n' + '-' * 55)
    if criterio == 'lucro':
        print(f'Lucro total estimado: R$ {resultado.valor_total:.2f}')
    elif criterio == 'avaliacao':
        print(f'Soma das avaliações: {resultado.valor_total:.1f}  (média: {mediaAval:.2f})')
    else:
        print(f'Popularidade total: {int(resultado.valor_total)}')

    print(f'Custo total: R$ {custoTotal:.2f}', end='')
    if orcamento:
        print(f' de R$ {orcamento:.2f}')
    else:
        print()
    print(f'Tempo total: {tempoTotal} min', end='')
    if tempoMax:
        print(f' de {int(tempoMax)} min')
    else:
        print()
    print(f'Avaliação média: {mediaAval:.2f} | Lucro estimado: R$ {sum(r.lucro for r in receitas):.2f}')

    print('\nJustificativa:')
    partes = [f'O menu foi escolhido por maximizar {criterioLabel}']
    limites = []
    if orcamento:
        limites.append(f'orçamento de R$ {orcamento:.2f} (usou R$ {custoTotal:.2f})')
    if tempoMax:
        limites.append(f'tempo de {int(tempoMax)} min (usou {tempoTotal} min)')
    if limites:
        partes.append('respeitando ' + ' e '.join(limites))
    print('  ' + ', '.join(partes) + '.')
    print('  A seleção é ótima (programação dinâmica - mochila 0/1), não uma aproximação gulosa.')


def montarMenuOtimizado(receitas):
    #Fluxo de interação da consulta "montar menu otimizado" (Módulo 6).
    criterio, criterioLabel = _escolherCriterio()
    if criterio is None:
        print('Critério inválido.')
        return

    print('\nRestrição de capacidade (peso da mochila):')
    print('1. Orçamento máximo (R$)')
    print('2. Tempo máximo de preparo (min)')
    print('3. Orçamento E tempo (as duas ao mesmo tempo)')
    tipo = input('Escolha: ').strip()

    orcamento = None
    tempoMax = None
    if tipo == '1':
        orcamento = _lerFloatPositivo('Orçamento máximo (R$): ')
        if orcamento is None:
            return
    elif tipo == '2':
        tempoMax = _lerFloatPositivo('Tempo máximo (min): ')
        if tempoMax is None:
            return
    elif tipo == '3':
        orcamento = _lerFloatPositivo('Orçamento máximo (R$): ')
        tempoMax = _lerFloatPositivo('Tempo máximo (min): ')
        if orcamento is None or tempoMax is None:
            return
    else:
        print('Opção inválida.')
        return

    disponiveis, max_raros, dificuldades = _lerRestricoesOpcionais(receitas)

    if tipo == '1':
        resultado = modulo6.consulta_melhor_menu_por_orcamento(
            receitas, orcamento, criterio, disponiveis, max_raros, dificuldades)
    elif tipo == '2':
        resultado = modulo6.consulta_melhor_menu_por_tempo(
            receitas, tempoMax, criterio, disponiveis, max_raros, dificuldades)
    else:
        resultado = modulo6.consulta_menu_por_tempo_e_orcamento(
            receitas, tempoMax, orcamento, criterio, disponiveis, max_raros, dificuldades)

    _exibirMenuOtimizado(resultado, criterio, criterioLabel, orcamento, tempoMax)


def modoChef(buscadorMod23, grafoDependencias, infoDependencias):
    receitas = list(buscadorMod23.receitas_originais.values())

    while True:
        limpar_tela()
        print('=' * 40)
        print('          MODO CHEF - GULOSO          ')
        print('=' * 40)
        print('1. Cardápio econômico por orçamento')
        print('2. Sugestões de pratos por critério')
        print('3. Sequência de produção do menu do dia (Módulo 5 - Kahn)')
        print('4. Montar menu otimizado (Módulo 6 - Mochila 0/1)')
        print('0. Voltar')

        opcao = input('\nEscolha uma opção: ').strip()

        if opcao == '1':
                
            orcamento =float(input('Digite o orçamento máximo: ').strip())

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

        elif opcao == '3':
            sequenciaProducaoMenuDoDia(grafoDependencias, infoDependencias, buscadorMod23)
            input('\nPressione Enter para voltar...')

        elif opcao == '4':
            montarMenuOtimizado(receitas)
            input('\nPressione Enter para voltar...')

        elif opcao == '0':
            break
        else:
            print('Opção inválida!')
            input('\nPressione Enter para voltar...')


