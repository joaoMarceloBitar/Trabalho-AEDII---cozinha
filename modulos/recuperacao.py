import os

def limpar_tela():
    os.system('clear')
    os.system('cls')

def mochila_01(receitas, tempo_maximo):
   
    # dp[w] guardará a avaliação máxima para o tempo w
    dp = [0.0] * (tempo_maximo + 1)
   
    # escolhidos[w] guardará a lista de receitas que compõem o dp[w]
    escolhidos = [[] for _ in range(tempo_maximo + 1)]
    for receita in receitas:
        peso = receita.tempo
        valor = receita.avaliacao
        
        if peso <= 0: continue
        
        # Percorre de trás para frente para não usar o mesmo item mais de uma vez
        for w in range(tempo_maximo, peso - 1, -1):
            if dp[w - peso] + valor > dp[w]:
                dp[w] = dp[w - peso] + valor
                escolhidos[w] = escolhidos[w - peso] + [receita]
                
    max_valor = dp[tempo_maximo]
    melhor_escolha = escolhidos[tempo_maximo]
    return max_valor, melhor_escolha

def mochila_fracionaria(receitas, tempo_maximo):
   
    # Ordena com base na razão Valor / Peso (Avaliação por Minuto)
    receitas_ordenadas = sorted(
        receitas, 
        key=lambda r: r.avaliacao / max(r.tempo, 1), 
        reverse=True
    )
    
    valor_total = 0.0
    tempo_atual = 0
    escolhidos = []
    
    for receita in receitas_ordenadas:
        peso = receita.tempo
        valor = receita.avaliacao
        
        if peso <= 0: continue
        
        if tempo_atual + peso <= tempo_maximo:
            # Pega inteiro
            tempo_atual += peso
            valor_total += valor
            escolhidos.append({
                "receita": receita,
                "fracao": 1.0,
                "tempo_usado": peso,
                "valor_obtido": valor
            })
        else:
            # Pega fracionário para preencher a mochila
            tempo_restante = tempo_maximo - tempo_atual
            if tempo_restante > 0:
                fracao = tempo_restante / peso
                valor_obtido = valor * fracao
                valor_total += valor_obtido
                escolhidos.append({
                    "receita": receita,
                    "fracao": fracao,
                    "tempo_usado": tempo_restante,
                    "valor_obtido": valor_obtido
                })
            break # Mochila encheu
            
    return valor_total, escolhidos

def menu_comparacao_mochilas(receitas):
    limpar_tela()
    print("=" * 60)
    print("   [RECUPERAÇÃO P1] MOCHILA 0/1 vs MOCHILA FRACIONÁRIA   ")
    print("=" * 60)
    print("Peso da Mochila = Tempo de Preparo (em minutos)")
    print("Valor do Item   = Avaliação (1.0 a 5.0)")
    print("O objetivo é maximizar a avaliação total dentro do tempo.\n")
    
    try:
        tempo_maximo = int(input("Digite o tempo máximo disponível na cozinha (ex: 120): ").strip())
    except ValueError:
        print("\nValor inválido. Retornando ao menu.")
        input("Pressione Enter para continuar...")
        return
    
    # Executa a Mochila 0/1
    valor_01, rec_01 = mochila_01(receitas, tempo_maximo)
    
    # Executa a Mochila Fracionária
    valor_frac, rec_frac = mochila_fracionaria(receitas, tempo_maximo)
    
    limpar_tela()
    print("=" * 60)
    print("                     RESULTADOS                     ")
    print("=" * 60)
    
    # Print 0/1
    print("\n--- ABORDAGEM 1: PROGRAMAÇÃO DINÂMICA (MOCHILA 0/1) ---")
    print("Restrição: Só podemos fazer a receita inteira.")
    tempo_gasto_01 = sum(r.tempo for r in rec_01)
    print(f"Avaliação Máxima Obtida: {valor_01:.2f}")
    print(f"Tempo Total Utilizado: {tempo_gasto_01} minutos")
    print("Receitas Escolhidas:")
    for r in rec_01:
        print(f"  - {r.nome[:25]:<25} | Tempo: {r.tempo:>3}min | Avaliação: {r.avaliacao:.1f}")
        
    # Print Fracionária
    print("\n--- ABORDAGEM 2: GULOSA (MOCHILA FRACIONÁRIA) ---")
    print("Restrição: Podemos fazer porções fracionárias da receita.")
    tempo_gasto_frac = sum(r['tempo_usado'] for r in rec_frac)
    print(f"Avaliação Máxima Obtida: {valor_frac:.2f}")
    print(f"Tempo Total Utilizado: {tempo_gasto_frac} minutos")
    print("Receitas Escolhidas:")
    for r in rec_frac:
        frac_pct = r['fracao'] * 100
        if r['fracao'] == 1.0:
            print(f"  - {r['receita'].nome[:25]:<25} | Tempo: {r['tempo_usado']:>3}min | Avaliação: {r['valor_obtido']:.2f} (100%)")
        else:
            print(f"  - {r['receita'].nome[:25]:<25} | Tempo: {r['tempo_usado']:>3}min | Avaliação: {r['valor_obtido']:.2f} ({frac_pct:.1f}%) [FRACIONADA]")

    print("\n" + "-" * 60)
    print("CONCLUSÃO:")
    print(f"A abordagem Fracionária garantiu um valor total de {valor_frac:.2f}.")
    print(f"A abordagem 0/1 garantiu um valor total de {valor_01:.2f}.")
    dif = valor_frac - valor_01
    if dif > 0.01:
        print(f"Isso demonstra que relaxar a restrição de integralidade permite agregar mais valor na mochila ({dif:.2f} a mais).")
        print("Note como a Mochila Fracionária pegou um pedaço da última receita para preencher o tempo exato.")
    else:
        print("Neste caso específico, a avaliação foi igual (a mochila pode ter sido preenchida exatamente com itens inteiros).")
        
    print("-" * 60)
    input("\nPressione Enter para voltar ao Menu Principal...")
