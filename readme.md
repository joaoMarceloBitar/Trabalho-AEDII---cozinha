# Trabalho-AEDII---cozinha

- Módulo 1 — Livro de Receitas: responsável por carregar, armazenar e listar as
receitas disponíveis no sistema. X

- Módulo 2 — Busca Rápida no Cardápio: responsável por permitir buscas
eficientes por nome, ID, categoria ou prefixo de receita.

- Módulo 3 — Organização dos Ingredientes: responsável por relacionar os
ingredientes às receitas cadastradas e permitir consultas por ingrediente.

- Módulo 5 (Desafio)— Recomendação do Chef: responsável por sugerir receitas ou
menus com base em critérios como custo, tempo de preparo, avaliação,
popularidade ou ingredientes disponíveis.


Os modos de interação representam formas de uso do sistema e podem reutilizar
funcionalidades implementadas nos módulos descritos anteriormente.


- 🕵️ Modo Investigação: encontrar receitas corrompidas
- O sistema deve permitir identificar possíveis inconsistências nas
receitas armazenadas.
Nesse modo, o usuário deverá ser capaz de:
2
- Verificar se uma receita foi alterada desde sua inserção no
sistema
- Identificar receitas com conteúdos inconsistentes ou
duplicados
- Detectar possíveis conflitos entre versões de uma mesma
receita
- Validar a integridade dos dados carregados a partir de
arquivos ou APIs
As verificações devem ser eficientes, mesmo para grandes volumes
de dados.


- 🍲 Modo Chef: recomendar pratos sob restrições
- O sistema deve auxiliar na escolha de receitas ou na composição de
menus com base em critérios definidos.
O usuário deverá ser capaz de:
- Selecionar receitas com base em restrições (ex: tempo
máximo, orçamento, dificuldade)
- Obter sugestões de pratos considerando múltiplos critérios
- Priorizar receitas com base em métricas como avaliação ou
popularidade
- Gerar combinações de receitas que atendam a um objetivo
específico (ex: menu econômico, menu rápido, etc.)
- As decisões devem ser justificáveis com base nos critérios
definidos.


- 🔍 Modo Consulta Rápida
- O sistema deve permitir a recuperação eficiente de receitas com
base em diferentes critérios.
O usuário deverá ser capaz de:
- Buscar receitas por nome (total ou parcial)
- Filtrar receitas por categoria
- Consultar receitas a partir de ingredientes específicos
- Localizar rapidamente receitas com base em identificadores
únicos
3
- O foco deste modo é garantir desempenho e eficiência na
recuperação das informações.

➢ Requisitos Obrigatórios :
O projeto deverá implementar do zero e utilizar, obrigatoriamente, pelo
menos 3 das 4 seguintes técnicas: Tabelas Hash; Árvore Trie (ou Árvore
Patrícia); Árvore B (ou B+); Algoritmo Guloso.
As estruturas de dados centrais do sistema deverão ser implementadas
pelo grupo, de forma a demonstrar compreensão de seu funcionamento.
O uso de bibliotecas prontas é permitido como apoio, desde que não
substitua integralmente as estruturas principais exigidas no trabalho.
Caso bibliotecas sejam utilizadas, o grupo deverá justificar sua escolha e
explicar claramente seu funcionamento e impacto na solução.
Bibliotecas também podem ser utilziadas para: leitura de arquivos;
consumo de API; manipulação de JSON ou CSV; interface; exibição de
dados.



# ROADMAP

## PASSO 1

fazer loop de interação:

ESBOÇO INTERAÇÃO USUÁRIO

- pesquisar
    - pesquisar por nome (trie)
    - pesquisar por categoria (dict ou hash)
    - pesquisar por ingrediente (dict)


## PASSO 2

organizar dados nas estruturas que vamos manipular

TRIE:
pegar os nomes das receitas q tao no json, isso vamos usar par:

- Buscar receitas por nome (total ou parcial) PRINCIPALMENTE USANDO TRIE

o resto das funções de busca escolhemos entre hash e trie, a que for mais conveniente

