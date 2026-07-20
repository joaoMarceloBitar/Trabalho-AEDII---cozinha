# abrir JSON
# transformar em objetos Receita
# devolver lista/dict

import json
import os
from receita.receita import Receita

def carregar_dados(caminho_arquivo="receitas_limpas.json"):
    
    if not os.path.exists(caminho_arquivo):
        print(f"Erro: Arquivo '{caminho_arquivo}' não encontrado!")
        print("ERRO NO CARREGAMENTO DOS DADOS!")
        return []
        
    with open(caminho_arquivo, 'r', encoding='utf-8') as f:
        dados_json = json.load(f)
        
    lista_receitas = []
    for item in dados_json:

        nova_receita = Receita(
            id_receita=item['id'],
            nome=item['nome'],
            categoria=item['categoria'],
            area=item['area'],
            ingredientes=item['ingredientes'],
            tempo=item['tempo_preparo_minutos'],
            custo=item['custo_estimado'],
            avaliacao=item['avaliacao'],
            dificuldade=item['dificuldade'],
            valor_venda=item.get('valor_venda', 0.0),
            popularidade=item.get('popularidade', 0)
        )
        lista_receitas.append(nova_receita)
        
    return lista_receitas