# Arquivo: estruturas/hash.py

class NoHash:
                                                    #encadeamento separado
    def __init__(self, chave, valor):
        self.chave = chave
        self.valor = valor
        self.proximo = None

class TabelaHash:
    def __init__(self, tamanho_tabela=100):
        self.tamanho = tamanho_tabela
        self.tabela = [None] * self.tamanho
        self.quantidade_elementos = 0 

    def _funcao_hash(self, chave):
        soma = 0
        for caractere in str(chave):
            soma += ord(caractere)
        return soma % self.tamanho

    def _redimensionar(self):
        tabela_antiga = self.tabela
        
        self.tamanho *= 2 
        self.tabela = [None] * self.tamanho
        self.quantidade_elementos = 0 

        # Percorre a tabela antiga e re-insere todos os nós com o novo cálculo
        for no_atual in tabela_antiga:
            atual = no_atual
            while atual is not None:
                self.inserir(atual.chave, atual.valor)
                atual = atual.proximo

    def inserir(self, chave, valor):
        # Se estiver 75% cheia, dobra de tamanho.
        fator_carga = self.quantidade_elementos / self.tamanho
        if fator_carga > 0.75:
            self._redimensionar()

        indice = self._funcao_hash(chave)
        novo_no = NoHash(chave, valor)

        if self.tabela[indice] is None:
            self.tabela[indice] = novo_no
            self.quantidade_elementos += 1 
        else:
            atual = self.tabela[indice]
            while atual.proximo is not None:
                if atual.chave == chave:
                    atual.valor = valor 
                    return
                atual = atual.proximo
            
            if atual.chave == chave:
                atual.valor = valor
            else:
                atual.proximo = novo_no
                self.quantidade_elementos += 1
                
    def buscar(self, chave):
        indice = self._funcao_hash(chave)
        atual = self.tabela[indice]

        while atual is not None:
            if atual.chave == chave:
                return atual.valor
            atual = atual.proximo
            
        return None