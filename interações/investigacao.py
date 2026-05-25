# 1. integridade com os dados da API
# 2. duplicatas de dados
# 3. corrupção
# 4. verificar se receita foi alterada desde que entrou no sistema

# 1 e 4 são bem parecidas, talvez possam ser a mesma função
from data.loader import carregar_dados

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

# verificar a integridade da hash de ids
# verificar a integridade da hash de categorias
# verificar a integridade da trie de nomes

# def verificaIntegridadeReceita(receita, receitaOriginal):
#     if receita.id_receita != receitaOriginal.id_receita:
#         return False
#     if receita.nome != receitaOriginal.nome:
#         return False
#     if receita.categoria != receitaOriginal.categoria:
#         return False
#     if receita.area != receitaOriginal.area:
#         return False
#     if set(receita.ingredientes) != set(receitaOriginal.ingredientes):
#         return False
#     if receita.tempo != receitaOriginal.tempo:
#         return False
#     if receita.custo != receitaOriginal.custo:
#         return False
#     if receita.avaliacao != receitaOriginal.avaliacao:
#         return False
#     if receita.dificuldade != receitaOriginal.dificuldade:
#         return False
    
#     return True


# def verificarIntegridadeLista( receitasAPI, buscadorMod23):

#     trie = buscadorMod23.trie_nomes
#     hashIds = buscadorMod23.hash_ids
#     hashCategorias = buscadorMod23.hash_categorias

#     erros = 0

#     for receita in receitasAPI:
      
#         temReceitaTrie = trie.buscar_por_prefixo(receita.nome)
#         if not temReceitaTrie:
#             print(f"Receita '{receita.nome}' não registrada na Trie")
#             erros += 1
       
#         temReceitaHashID = hashIds.buscar(receita.id)  
#         if temReceitaHashID:
#             if not verificaIntegridadeReceita(receita, temReceitaHashID):
#                 print(f"Receita '{receita.nome}' (ID: {receita.id}) corrompida ou alterada na Hash de IDs")
#                 erros += 1
#         else:
#             print(f"Receita '{receita.nome}' (ID: {receita.id}) não registrada na Hash de IDs")
       
#         temReceitaHashCategoria = hashCategorias.buscar(receita.categoria)
#         if not temReceitaHashCategoria:
#             print(f"Receita '{receita.nome}' (Categoria: {receita.categoria}) não registrada na Hash de Categorias")
#             erros += 1
        

#     print(f"Total de erros encontrados: {erros}")
