import requests
import json
import random 

def buscar_receitas():
    letras = ['a', 'b', 'c', 'd', 'e', 'f']
    todas_receitas = {}

    print("Iniciando a extração e limpeza de dados...")

    for letra in letras:
        url = f"https://www.themealdb.com/api/json/v1/1/search.php?f={letra}"
        resposta = requests.get(url)
        
        if resposta.status_code == 200:
            dados = resposta.json()
            if dados.get('meals'):
                for prato in dados['meals']:
                    
                    ingredientes_limpos = []
                    for i in range(1, 21):
                        ingrediente = prato.get(f"strIngredient{i}")
                        # Verifica se a string existe e não é apenas um espaço em branco
                        if ingrediente and ingrediente.strip():
                            # Salva tudo em minúsculo para facilitar a busca na Árvore Trie depois
                            ingredientes_limpos.append(ingrediente.strip().lower())

                   
                    receita_limpa = {
                        "id": prato["idMeal"],
                        "nome": prato["strMeal"],
                        "categoria": prato["strCategory"],
                        "area": prato["strArea"],
                        "ingredientes": ingredientes_limpos,
                        
                       
                        "tempo_preparo_minutos": random.randint(15, 120),
                        "custo_estimado": round(random.uniform(15.0, 150.0), 2),
                        "avaliacao": round(random.uniform(3.5, 5.0), 1),
                        "dificuldade": random.choice(["Fácil", "Média", "Difícil"])
                    }
                    
                   
                    todas_receitas[receita_limpa['id']] = receita_limpa
                    
                    
                    
                    if len(todas_receitas) == 50:
                        break
                        
            print(f"Letra '{letra}' processada. Total acumulado: {len(todas_receitas)}")
        else:
            print(f"Erro ao buscar a letra {letra}")
            
        if len(todas_receitas) == 50:
            print("\nLimite exato de 50 receitas atingido! Abortando as próximas letras.")
            break

    lista_final = list(todas_receitas.values())

 
    with open('receitas_limpas.json', 'w', encoding='utf-8') as arquivo:
        json.dump(lista_final, arquivo, indent=4, ensure_ascii=False)

    print(f"Sucesso! {len(lista_final)} receitas limpas salvas em 'receitas_limpas.json'.")

if __name__ == "__main__":
    buscar_receitas()