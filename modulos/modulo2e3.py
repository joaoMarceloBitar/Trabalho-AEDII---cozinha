# busca por nome
# busca por prefixo
# busca por categoria
# busca por ID
# busca por ingredientes 
#modulo 2 e 3

from estruturas.trie import ArvoreTrie
from estruturas.hash import TabelaHash

class BuscadorCardapio:
    def __init__(self, lista_receitas):
        self.receitas_originais = {receita.id: receita for receita in lista_receitas} 
        
        # Inicializando nossas estruturas de dados 
        self.trie_nomes = ArvoreTrie()
        self.hash_ids = TabelaHash(tamanho_tabela=100)
        self.hash_categorias = TabelaHash(tamanho_tabela=50)
        self.hash_ingredientes = TabelaHash(tamanho_tabela=200) # Módulo 3 

        self._indexar_dados(lista_receitas)

    def _indexar_dados(self, lista_receitas):
       
        for receita in lista_receitas:
            self.trie_nomes.inserir(receita.nome, receita.id)
            self.hash_ids.inserir(receita.id, receita)
            cat_atual = self.hash_categorias.buscar(receita.categoria.lower())
            
            if cat_atual is None:
                self.hash_categorias.inserir(receita.categoria.lower(), [receita.id])
            else:
                cat_atual.append(receita.id)
                self.hash_categorias.inserir(receita.categoria.lower(), cat_atual)

            for ingrediente in receita.ingredientes:
                ing_atual = self.hash_ingredientes.buscar(ingrediente.lower())
                if ing_atual is None:
                    self.hash_ingredientes.inserir(ingrediente.lower(), [receita.id])
                else:
                    if receita.id not in ing_atual:
                        ing_atual.append(receita.id)
                        self.hash_ingredientes.inserir(ingrediente.lower(), ing_atual)

    

    def _converter_ids_para_receitas(self, lista_ids):
        #Função auxiliar para transformar uma lista de IDs de volta em objetos Receita
        if not lista_ids:
            return []
        return [self.receitas_originais[id_rec] for id_rec in lista_ids]

    def buscar_por_nome_ou_prefixo(self, termo):
        ids_encontrados = self.trie_nomes.buscar_por_prefixo(termo)
        return self._converter_ids_para_receitas(ids_encontrados)

    def buscar_por_id(self, id_receita):
        return self.hash_ids.buscar(id_receita)

    def buscar_por_categoria(self, categoria):
        ids_encontrados = self.hash_categorias.buscar(categoria.lower())
        return self._converter_ids_para_receitas(ids_encontrados)

    def buscar_por_ingrediente(self, ingrediente):
        #busca por ingredientes, cobre modulo3
        ids_encontrados = self.hash_ingredientes.buscar(ingrediente.lower())
        return self._converter_ids_para_receitas(ids_encontrados)