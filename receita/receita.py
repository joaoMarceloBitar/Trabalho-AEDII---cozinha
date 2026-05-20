class Receita:
    def __init__(self, id_receita, nome, categoria, area, ingredientes, tempo, custo, avaliacao, dificuldade):
        self.id = id_receita
        self.nome = nome
        self.categoria = categoria
        self.area = area
        self.ingredientes = ingredientes
        self.tempo = tempo
        self.custo = custo
        self.avaliacao = avaliacao
        self.dificuldade = dificuldade

    def __str__(self):
        return f"ID: {self.id} | {self.nome} - {self.categoria} ({self.tempo} min | R$ {self.custo:.2f})"