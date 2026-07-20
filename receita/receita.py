class Receita:
    def __init__(self, id_receita, nome, categoria, area, ingredientes, tempo, custo, avaliacao, dificuldade, valor_venda=0.0, popularidade=0):
        self.id = id_receita
        self.nome = nome
        self.categoria = categoria
        self.area = area
        self.ingredientes = ingredientes
        self.tempo = tempo
        self.custo = custo
        self.avaliacao = avaliacao
        self.dificuldade = dificuldade
        self.valor_venda = valor_venda
        self.popularidade = popularidade

    @property
    def lucro(self):
        # Lucro esperado, derivado em runtime (nunca persistido no JSON).
        return self.valor_venda - self.custo

    def __str__(self):
        return f"ID: {self.id} | {self.nome} - {self.categoria} ({self.tempo} min | R$ {self.custo:.2f})"