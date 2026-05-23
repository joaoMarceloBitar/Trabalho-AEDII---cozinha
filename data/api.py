import requests
import json
import random

def extrair_dados_api():
    letras = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    todas_receitas = {}

    print("Iniciando a extração e limpeza de dados da API TheMealDB...")

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
                        if ingrediente and ingrediente.strip():
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
                    
                    if len(todas_receitas) == 1000:
                        break
                        
            print(f"Letra '{letra}' processada. Total acumulado: {len(todas_receitas)}")
        else:
            print(f"Erro ao buscar a letra {letra}")
            
        if len(todas_receitas) == 1000:
            print("\nLimite exato de 1000 receitas atingido! Abortando buscas adicionais.")
            break

    lista_final = list(todas_receitas.values())

  
    with open('receitas_limpas.json', 'w', encoding='utf-8') as arquivo:
        json.dump(lista_final, arquivo, indent=4, ensure_ascii=False)

    print(f"Sucesso! {len(lista_final)} receitas salvas no arquivo 'receitas_limpas.json'.")

if __name__ == "__main__":
    extrair_dados_api()