#modulo 1
from data.loader import carregar_dados

def carregar_livro():

    print("Carregando base de dados do Livro de Receitas...")
    receitas = carregar_dados("receitas_limpas.json")
    return receitas

def listar_livro(receitas):
    
    if not receitas:
        print("Nenhuma receita encontrada no sistema.")
        return
        
    for receita in receitas:
        print(receita)
        
    print("="*50)