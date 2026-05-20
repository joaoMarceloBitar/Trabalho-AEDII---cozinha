class Receita:
    def __init__(self, idMeal, nome, categoria, area, tags):
        self.id = idMeal
        self.nome = nome
        self.categoria = categoria
        self.area = area
        self.tags = tags

    def __str__(self):
        return f"{self.nome} - {self.categoria}"