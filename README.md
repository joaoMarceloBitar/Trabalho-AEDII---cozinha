# Trabalho-AEDII - (Cozinha)

**Integrantes**
- João Marcelo Bitar
- Pedro de Freitas Scheeren

**Link do Repositório:** -> github.com/joaoMarceloBitar/Trabalho-AEDII---cozinha

## Instruções de Execução

1. Certifique-se de ter o Python 3 instalado em sua máquina.
2. Clone o repositório para o seu computador.
3. Pelo terminal, navegue até a pasta raiz do projeto.
4. Execute o arquivo principal do sistema:

python3 main.py

O sistema irá automaticamente carregar a base de dados em memória (`receitas_limpas.json`) e exibir o Menu Principal interativo.

## Fonte de Dados

A fonte de dados escolhida para este projeto foi a **TheMealDB API**. Um script de extração obteve as receitas, realizou um processo de limpeza e salvou as informações estruturadas localmente no arquivo `receitas_limpas.json`. Isso permite testes rápidos e eficiência no carregamento das estruturas de dados em memória, sem depender de acesso externo durante a execução do programa.

## Estruturas de Dados e Algoritmos Implementados

O projeto implementa 3 das 4 técnicas requisitadas. Abaixo, detalhamos onde cada uma foi aplicada e a justificativa para sua escolha.

### 1. Árvore Trie

* **Onde foi aplicada:** No Módulo 2 (Busca Rápida), especificamente na funcionalidade de buscar receitas pelo seu Nome ou Prefixo.
* **Justificativa:** A Árvore Trie é a estrutura mais otimizada para recuperação e pesquisa de textos por prefixo (autocompletar). Como o tempo de busca depende apenas do tamanho da string pesquisada, permite que o usuário digite as primeiras letras do prato e encontre os resultados de forma quase instantânea (complexidade O(L)), independentemente da quantidade de receitas cadastradas.

### 2. Tabelas Hash

* **Onde foi aplicada:** Nos Módulos 2 e 3 (Buscas e Organização), nas funcionalidades de busca por ID, Categoria e Ingrediente.
* **Justificativa:** A Tabela Hash foi escolhida para esses casos pois proporciona buscas exatas com complexidade de tempo média O(1). Como IDs, Categorias e Ingredientes servem como chaves de indexação direta, as consultas retornam a lista de receitas correspondentes imediatamente, evitando a necessidade de varrer toda a base de dados linearmente.

### 3. Algoritmo Guloso

* **Onde foi aplicado:** No Módulo 4 (Menu Rápido) e interações do "Modo Chef".
* **Justificativa:** Aplicado para a montagem e recomendação de um menu maximizado sob a restrição de tempo máximo de preparo. A abordagem gulosa ordena os pratos pelo menor tempo de preparo e os seleciona iterativamente até o limite de tempo estabelecido acabar. A justificativa para a sua escolha é a capacidade de gerar uma solução excelente (em alguns casos a ótima) de forma muito rápida, selecionando sempre a melhor opção local a cada passo sem as pesadas chamadas recursivas de algoritmos exatos de otimização.

No Modo Chef é usado como critério de decisão das seleções de menu personalizadas, onde baseado em uma limitação e um objetivo, as receitas são selecionadas e filtradas pensando na melhor individualmente a cada iteração do algorítmo  

## [RECUPERAÇÃO P1] Diferença entre Mochila 0/1 e Fracionária

**Questão Escolhida:** Recuperação da Questão 5 da prova (Diferença entre Mochila 0/1 e Mochila Fracionária).

### Explicação Teórica e Arquitetural
Durante a prova, uma das dificuldades na Questão 5 foi justamente diferenciar a aplicabilidade e as limitações do Problema da Mochila 0/1 (que não permite frações) em relação à Mochila Fracionária (que permite pegar pedaços dos itens).

Na Mochila 0/1, não podemos usar um algoritmo Guloso, pois a escolha baseada apenas na melhor proporção valor/peso não garante a solução ótima devido aos espaços vazios que podem sobrar. Para garantir a resposta correta, precisamos usar Programação Dinâmica (DP), testando todas as combinações viáveis, o que demanda mais esforço computacional e exige que os pesos sejam inteiros.

Já na Mochila Fracionária, o algoritmo Guloso funciona perfeitamente, garantindo a solução ótima ao ordenarmos os itens por valor/peso e pegando frações para preencher exatamente o espaço restante da mochila, otimizando o preenchimento a 100%.

**Implementação no Projeto:** 
No nosso sistema de receitas, adaptamos essa lógica da seguinte forma:
- **Peso da Mochila =** Tempo de Preparo da receita (`tempo_preparo_minutos`).
- **Valor do Item =** Avaliação da receita (`avaliacao`).
- **Capacidade =** Tempo total disponível na cozinha.

O algoritmo 0/1 foi feito com DP em matriz 1D e obriga que a receita seja feita por inteiro. O algoritmo Fracionário foi feito com lógica gulosa, ordenando a avaliação por tempo gasto, permitindo "preparar metade da receita" e receber metade da avaliação, preenchendo assim todos os minutos disponíveis perfeitamente e garantindo, em alguns casos, uma avaliação total maior que a da 0/1.

### Passo a Passo para Teste (Avaliação)

1. No terminal da raiz do projeto, execute o comando:

   python3 main.py

2. Após carregar a base de dados, pressione Enter para abrir o **MENU PRINCIPAL**.
3. Selecione a opção **3. [BONUS] Comparação Mochila 0/1 e Fracionária**.
4. Quando solicitado, digite o tempo máximo disponível (ex: `120`) e pressione Enter.
5. O sistema fará o cálculo e exibirá as escolhas de cada abordagem. Observe como a abordagem Fracionária fraciona (ex: 50% ou 20%) o último prato inserido para maximizar o ganho, atingindo, em muitos casos, um valor total superior à abordagem 0/1.