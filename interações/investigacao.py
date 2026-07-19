# 1. integridade com os dados da API
# 2. duplicatas de dados
# 3. corrupção
# 4. verificar se receita foi alterada desde que entrou no sistema

# 1 e 4 são bem parecidas, talvez possam ser a mesma função
import os

from data.loader import carregar_dados
from modulos.modulo5 import detectar_erro_dependencia, preparos_antecedentes


def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')


def dadosNormalizados(x):
    return str(x or "").strip().lower()


def verificarIntegridadeLista(buscadorMod23):
    erros = 0
    receitasOriginais = buscadorMod23.receitas_originais

    for idReceita in receitasOriginais.keys():
        receitaObj = receitasOriginais[idReceita]
        idNormalizado = dadosNormalizados(idReceita)

        receitaHashId = buscadorMod23.buscar_por_id(idReceita)
        if receitaHashId is None:
            print(f" receita ID {idReceita} não registrada na Hash de IDs")
            erros += 1
        else:
            if dadosNormalizados(receitaHashId.id) != idNormalizado:
                print(f" receita ID {idReceita} diferente do registro na Hash de IDs")
                erros += 1

        categoriaOriginal = receitaObj.categoria
        listaObjetosCategoria = buscadorMod23.buscar_por_categoria(categoriaOriginal) or []
        idsCategoria = [dadosNormalizados(r.id) for r in listaObjetosCategoria]
        if idNormalizado not in idsCategoria:
            print(f" receita ID {idReceita} não encontrada na categoria '{categoriaOriginal}'")
            erros += 1

        ingredientesOriginais = set(receitaObj.ingredientes)
        for ingrediente in ingredientesOriginais:
            listaReceitasIngrediente = buscadorMod23.buscar_por_ingrediente(ingrediente) or []
            idsIngrediente = [dadosNormalizados(r.id) for r in listaReceitasIngrediente]
            if idNormalizado not in idsIngrediente:
                print(f" receita ID {idReceita} não encontrada no índice de ingrediente '{ingrediente}'")
                erros += 1

        nomeOriginal = receitaObj.nome
        idsEncontradosTrie = buscadorMod23.trie_nomes.buscar_por_prefixo(nomeOriginal) or []
        idsEncontradosTrie_norm = [dadosNormalizados(i) for i in idsEncontradosTrie]
        if idNormalizado not in idsEncontradosTrie_norm:
            print(f" receita ID {idReceita} não encontrada na Trie de nomes")
            erros += 1
    print(f"Total de erros encontrados: {erros}")

# --- Módulo 5 (Oficina de Produção) --------------------------------------
# Estas funções só coletam entrada do usuário e formatam a saída; a regra
# de negócio (grafo, ciclo, ancestrais) vive em modulos/modulo5.py.

def consultarErroDependencia(grafoDependencias, infoDependencias, buscadorMod23):
    resultado = detectar_erro_dependencia(grafoDependencias, infoDependencias, buscadorMod23)

    print('\n--- Existe algum erro de dependência? ---')
    if not resultado.tem_erro:
        print('Nenhuma inconsistência encontrada: o grafo de dependências é válido (sem ciclos).')
    else:
        print('Erro de cadastro encontrado! O seguinte ciclo de dependências impede a produção:')
        print('  ' + ' -> '.join(resultado.ciclo))


def consultarPreparosAntecedentes(grafoDependencias, infoDependencias, buscadorMod23):
    idReceita = input('\nDigite o ID da receita: ').strip()
    resultado = preparos_antecedentes(grafoDependencias, infoDependencias, buscadorMod23, idReceita)

    if not resultado.sucesso:
        print(f'\n{resultado.mensagem_erro}')
        return

    if not resultado.preparos:
        print('\nEssa receita não depende de nenhum preparo intermediário cadastrado.')
        return

    print('\nPreparos que precisam ser concluídos antes, em ordem:')
    for indice, nome in enumerate(resultado.preparos, start=1):
        print(f'  {indice}. {nome}')


def modoInvestigacao(buscadorMod23, grafoDependencias, infoDependencias):
    while True:
        limpar_tela()
        print('=' * 40)
        print('         MODO INVESTIGAÇÃO         ')
        print('=' * 40)
        print('1. Verificar integridade dos índices (T1)')
        print('2. Detectar erro de dependência entre preparos')
        print('3. Preparos antecedentes de uma receita')
        print('0. Voltar')

        opcao = input('\nEscolha uma opção: ').strip()

        if opcao == '1':
            verificarIntegridadeLista(buscadorMod23)
            input('\nPressione Enter para voltar...')
        elif opcao == '2':
            consultarErroDependencia(grafoDependencias, infoDependencias, buscadorMod23)
            input('\nPressione Enter para voltar...')
        elif opcao == '3':
            consultarPreparosAntecedentes(grafoDependencias, infoDependencias, buscadorMod23)
            input('\nPressione Enter para voltar...')
        elif opcao == '0':
            break
        else:
            print('Opção inválida!')
            input('\nPressione Enter para voltar...')
