# Guia simples das colunas

A tabela mostra somente informações do Google Trends e cálculos feitos sobre a
curva dos últimos três meses. Cada palavra-chave é pesquisada sozinha, sem texto
adicional.

## Palavra-chave

- **Formato:** texto.
- **Origem:** `data/input_keywords.json`.
- **Significado:** termo enviado ao Google Trends.

## Interesse médio

- **Formato:** índice decimal de 0 a 100.
- **Origem:** média da série retornada por `interest_over_time()`.
- **Significado:** intensidade sustentada do interesse durante os três meses.

## Interesse recente

- **Formato:** índice inteiro de 0 a 100.
- **Origem:** último período completo retornado pelo Google Trends.
- **Significado:** situação mais recente do interesse pela palavra.

## Pico

- **Formato:** índice inteiro de 0 a 100.
- **Origem:** maior valor da curva nos três meses.
- **Significado:** ponto de maior atenção observado no período.

## Tendência

- **Formato:** `CRESCENTE`, `ESTÁVEL` ou `DECRESCENTE`.
- **Origem:** regressão linear calculada pela aplicação sobre a curva.
- **Significado:** direção geral da série, reduzindo o peso de oscilações
  isoladas.

## Variação da curva

- **Formato:** pontos do índice, positivos ou negativos.
- **Origem:** diferença projetada pela linha de tendência entre o início e o fim
  dos três meses.
- **Significado:** força aproximada da subida ou da queda.

## Relevância

- **Formato:** pontuação de 0 a 100.
- **Origem:** cálculo da aplicação:
  - 50% do interesse médio;
  - 30% do interesse recente;
  - 20% da direção da curva.
- **Significado:** resumo da presença, atualidade e trajetória da palavra.

## Fonte

- **Formato:** texto.
- **Valor esperado:** `GOOGLE_TRENDS`.
- **Significado:** confirma que os dados vieram do Google Trends via `pytrends`.

## Limitação importante

O Google Trends normaliza cada palavra individualmente entre 0 e 100. Portanto,
o relatório avalia o comportamento da curva de cada termo, mas não informa
volume absoluto de buscas e não garante que uma palavra com score maior seja
mais pesquisada em números absolutos.

## Como usar os tooltips

Passe o mouse sobre o círculo **i** ao lado do cabeçalho. Pelo teclado, pressione
`Tab` até chegar ao círculo para exibir a mesma explicação.
