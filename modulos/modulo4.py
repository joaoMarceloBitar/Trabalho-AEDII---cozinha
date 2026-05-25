#modulo 5 do pdf

def menu_rapido(receitas, tempo_maximo):
   
    # filtra apenas as receitas que cabem no tempo máximo estipulado
    receitas_validas = [r for r in receitas if r.tempo <= tempo_maximo]

    # ordenação Gulosa (Menor tempo primeiro)
    receitas_ordenadas = sorted(
        receitas_validas, 
        key=lambda r: r.tempo
    )

    menu_selecionado = []
    tempo_total = 0
    
    # seleção Gulosa
    for receita in receitas_ordenadas:
        if tempo_total + receita.tempo <= tempo_maximo:
            menu_selecionado.append(receita)
            tempo_total += receita.tempo

    return menu_selecionado, tempo_total

def imprimir_menu(menu_selecionado, tempo_total):
    
    if not menu_selecionado:
        print("Não foi possível montar um cardápio com o tempo disponível.")
        return

    print("=" * 50)
    print(f"       CARDÁPIO RÁPIDO (Total: {tempo_total} min)")
    print("=" * 50)

    for receita in menu_selecionado:
        print(f"ID: {receita.id} | Nome: {receita.nome}")
        print(f"    Tempo: {receita.tempo} min | Dificuldade: {receita.dificuldade}")
        
    print("=" * 50)