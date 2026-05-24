import os
from data.loader import carregar_dados
from interações.investigacao import verificarIntegridadeLista
from modulos.modulo1 import listar_livro
from modulos.modulo2e3 import BuscadorCardapio

def limpar_tela():
    os.system('clear')


# SUBMENUS DE CONSULTA (Módulos 2 e 3)

def menu_consultas(buscador):
    while True:
        limpar_tela()
        print("-" * 40)
        print("   MÓDULOS 2 e 3: CONSULTAS RÁPIDAS   ")
        print("-" * 40)
        print("1. Buscar por Nome ou Prefixo (Trie)")
        print("2. Buscar por ID (Hash)")
        print("3. Buscar por Categoria (Hash)")
        print("4. Buscar por Ingrediente (Hash)")
        print("0. Voltar aos Módulos")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            termo = input("\nDigite o nome ou prefixo: ").strip()
            resultados = buscador.buscar_por_nome_ou_prefixo(termo)
            exibir_resultados(resultados)
            input("\nPressione Enter para voltar...")

        elif opcao == "2":
            id_busca = input("\nDigite o ID da receita: ").strip()
            receita = buscador.buscar_por_id(id_busca)
            if receita:
                print(f"\nReceita Encontrada:\n{receita}")
                print(f"Ingredientes: {', '.join(receita.ingredientes)}")
            else:
                print("ID não encontrado no sistema.")
            input("\nPressione Enter para voltar...")

        elif opcao == "3":
            categoria = input("\nDigite a categoria: ").strip()
            resultados = buscador.buscar_por_categoria(categoria)
            exibir_resultados(resultados)
            input("\nPressione Enter para voltar...")

        elif opcao == "4":
            ingrediente = input("\nDigite o ingrediente: ").strip()
            resultados = buscador.buscar_por_ingrediente(ingrediente)
            exibir_resultados(resultados)
            input("\nPressione Enter para voltar...")

        elif opcao == "0":
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            input("\nPressione Enter para voltar...")

def exibir_resultados(resultados):
    if resultados:
        print(f"\n{len(resultados)} receita(s) encontrada(s):")
        for rec in resultados:
            print(rec)
    else:
        print("\nNenhuma receita encontrada para a busca.")


# MENUS INTERMEDIÁRIOS (Módulos vs Interações)

def menu_modulos(receitas, buscador):
    while True:
        limpar_tela()
        print("=" * 40)
        print("          MÓDULOS DO SISTEMA          ")
        print("=" * 40)
        print("1. Módulo 1: Livro de Receitas (Listar)")
        print("2. Módulos 2 e 3: Buscas e Filtros")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            limpar_tela()
            print("--- LIVRO DE RECEITAS ---\n")
            listar_livro(receitas)
            input("\nPressione Enter para voltar...")
        elif opcao == "2":
            menu_consultas(buscador)
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida!")
            input("\nPressione Enter para voltar...")

def menu_interacoes(receitas, buscadorMod23):
    while True:
        limpar_tela()
        print("=" * 40)
        print("         MODOS DE INTERAÇÃO         ")
        print("=" * 40)
        print("1. Modo Investigação (Integridade/Hash)")
        print("2. Modo Chef (Algoritmo Guloso)")
        print("0. Voltar ao Menu Principal")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            verificarIntegridadeLista(buscadorMod23)
            input("\nPressione Enter para voltar...")
        elif opcao == "2":
           
            input("\nPressione Enter para voltar...")
        elif opcao == "0":
            break
        else:
            print("\nOpção inválida!")
            input("\nPressione Enter para voltar...")


# MENU PRINCIPAL E INICIALIZAÇÃO

def iniciar_sistema():
    limpar_tela()
    print("=" * 50)
    print("       TRABALHO DESAFIO NA COZINHA - AED 2       ")
    print("=" * 50)
   
    print("\nCarregando base de dados...")
    receitas = carregar_dados("receitas_limpas.json")
    
    if not receitas:
        print("Encerrando o sistema. Verifique a base de dados.")
        return

    print(f"Sucesso: {len(receitas)} receitas carregadas na memória!")
    
    print("\nIndexando estruturas de dados (Trie e Hash)...")
    buscador = BuscadorCardapio(receitas)
    print("Sistema pronto para uso!")
    
    input("\nPressione Enter para iniciar...")
    
    while True:
        limpar_tela()
        print("#" * 40)
        print("             MENU PRINCIPAL             ")
        print("#" * 40)
        print("1. Acessar Módulos do Sistema")
        print("2. Acessar Modos de Interação")
        print("0. Sair")
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            menu_modulos(receitas, buscador)
        elif opcao == "2":
            menu_interacoes(buscador)
        elif opcao == "0":
            limpar_tela()
            print("Encerrando o sistema. Até breve, Chef!\n")
            break
        else:
            print("\nOpção inválida! Tente novamente.")
            input("\nPressione Enter para voltar...")

if __name__ == "__main__":
    iniciar_sistema()