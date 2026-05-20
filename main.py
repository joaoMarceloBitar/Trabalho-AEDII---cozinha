from data.loader import carregar_dados
from modulos.livro_receitas import carregar_livro, listar_livro

def iniciar_sistema():
    
    print("   TRABALHO DESAFIO NA COZINHA - AED 2  ")
   
    
    print("Carregando base de dados...\n")
    receitas = carregar_dados("receitas_limpas.json")
    
    if not receitas:
        print("Encerrando o sistema. Verifique a base de dados.")
        return

    print(f"Sucesso: {len(receitas)} receitas carregadas na memória!\n")
    
    while True:
        print("\n--- MENU PRINCIPAL ---")
        print("1. Listar todas as Receitas (Módulo 1)")
        print("0. Sair")
        
        opcao = input("Escolha uma opção: ")
        
        if opcao == "1":
            print("\n--- LIVRO DE RECEITAS ---")
            listar_livro(receitas)
                
        elif opcao == "0":
            print("\nEncerrando o sistema. Até breve, Chef!")
            break
        else:
            print("\nOpção inválida! Tente novamente.")

if __name__ == "__main__":
    iniciar_sistema()