class NoTrie:
    def __init__(self):
        self.filhos = {}
        self.fim_de_palavra = False
        self.ids_receitas = []

class ArvoreTrie:
    def __init__(self):
        self.raiz = NoTrie() #raiz nó vazio

    def inserir(self, nome_receita, id_receita):
        palavra = nome_receita.lower()
        no_atual = self.raiz
        
        for caractere in palavra:
            # Se a letra não existe no nó atual, criamos um novo nó
            if caractere not in no_atual.filhos:
                no_atual.filhos[caractere] = NoTrie()
            # Avançamos para o nó da letra
            no_atual = no_atual.filhos[caractere]
            
        # Terminamos de percorrer a palavra
        no_atual.fim_de_palavra = True
        
        # Adicionamos o ID (evitando IDs duplicados no mesmo nó)
        if id_receita not in no_atual.ids_receitas:
            no_atual.ids_receitas.append(id_receita)

    def buscar_por_prefixo(self, prefixo):
        prefixo = prefixo.lower()
        no_atual = self.raiz
        
        # 1. Desce na árvore até o fim do prefixo
        for caractere in prefixo:
            if caractere not in no_atual.filhos:
                # Se quebrou o caminho antes de terminar o prefixo, não achou nada
                return [] 
            no_atual = no_atual.filhos[caractere]
            
        # 2. Se encontrou o prefixo, coleta todos os IDs pendurados abaixo deste nó
        resultados = []
        self._coletar_ids(no_atual, resultados)
        
        return resultados

    def _coletar_ids(self, no, resultados):
        if no.fim_de_palavra:
            resultados.extend(no.ids_receitas)
            
        # Chama a função para todos os filhos do nó atual
        for filho in no.filhos.values():
            self._coletar_ids(filho, resultados)