# Análise de falha da integração com Google Trends

## Resumo executivo

A aplicação não coletava dados do Google Trends. Quando `DATA_SOURCE` recebia
`GOOGLE_TRENDS`, o adaptador chamava diretamente o cliente `MOCK`, portanto os
valores exibidos continuavam sendo sintéticos. A dependência `pytrends` também
não estava instalada e não existia qualquer requisição ao serviço.

A correção implementada adiciona `pytrends 4.9.2`, consulta
`interest_over_time()`, trata falhas de conexão e HTTP 429, remove períodos
parciais e grava o resultado em `data/keyword_trends_report.json`.

## O que estava quebrado

### 1. A fonte padrão era simulada

O arquivo `.env.example` definia `DATA_SOURCE=MOCK`. Sem um arquivo `.env` que
substituísse esse valor, o fluxo principal nunca selecionava Google Trends.

### 2. O adaptador do Google Trends devolvia o mock

`integrations/google_trends_client.py` não criava uma sessão `TrendReq`, não
montava um payload e não consultava `interest_over_time()`. Com o fallback
habilitado pelo arquivo principal, a função retornava imediatamente os números
produzidos por `mock_client.py`.

Esses números são derivados de um hash da palavra-chave. Eles são repetíveis e
úteis para testar a interface, mas não possuem relação com pesquisas reais.

### 3. A dependência necessária não existia

Nem `pyproject.toml` nem `requirements.txt` declaravam `pytrends`. Mesmo que o
stub tentasse importar `TrendReq`, a execução terminaria com
`ModuleNotFoundError`.

### 4. O contrato do relatório representava Google Ads

O relatório esperava volume mensal, competição e valores de lance. Google
Trends não fornece essas métricas. Ele fornece um índice relativo normalizado
de 0 a 100 dentro do período, região e conjunto de termos consultados.

Tratar esse índice como volume mensal produziria um relatório semanticamente
incorreto. Por isso a saída do Trends agora usa:

- `average_interest`;
- `peak_interest`;
- `latest_interest`;
- `trend_direction`;
- `trend_change`;
- `relevance_score`;
- `timeline`.

### 5. Não havia tratamento de falhas remotas

O código não diferenciava erro de conexão, resposta inválida e bloqueio
temporário HTTP 429. Também não havia espera progressiva entre tentativas.

## Por que a ausência do pytrends invalidava a coleta

`pytrends` é uma pseudo-API não oficial que reproduz as requisições usadas pela
interface pública do Google Trends. Sem ela — ou sem outra implementação HTTP
equivalente — a aplicação não possui um cliente capaz de:

1. iniciar a sessão esperada pelo Google Trends;
2. construir o payload com termos, período e região;
3. obter os tokens usados nas consultas;
4. baixar a série de interesse ao longo do tempo;
5. converter a resposta para uma estrutura tabular.

No cenário anterior não existia caminho alternativo para executar essas
etapas. Selecionar `GOOGLE_TRENDS` apenas trocava o ramo do programa antes de
voltar ao gerador sintético.

## Correção implementada

### Utilitário isolado

O módulo `utils/google_trends.py` concentra:

- validação de listas extensas de palavras-chave;
- consulta de cada palavra sem modificar seu texto;
- consulta individual de cada palavra-chave sem modificadores;
- configuração de idioma, fuso, região e período;
- criação de `TrendReq`;
- chamada de `build_payload()` e `interest_over_time()`;
- remoção de linhas marcadas como `isPartial`;
- transformação da série em valores JSON;
- retentativas com backoff exponencial;
- espera aleatória de 5 a 20 segundos entre consultas remotas;
- cache persistente atualizado após cada palavra-chave;
- erros específicos para conexão, HTTP 429 e respostas inválidas.

Cada requisição contém somente a palavra-chave original. A pontuação resume a
média, o interesse recente e a direção da curva nos últimos três meses. Ela
avalia o comportamento temporal do termo, não volume absoluto entre palavras.

### Tratamento de HTTP 429

O utilitário usa retentativas próprias, em vez do retry interno do `pytrends`.
Na versão 4.9.2, o retry interno ainda passa `method_whitelist` ao urllib3,
argumento incompatível com versões atuais da biblioteca.

Com os valores padrão, as esperas são de 5, 10 e 20 segundos. Se a quarta
tentativa também receber 429, a aplicação encerra com uma mensagem clara. O
programa não tenta contornar o bloqueio com rotação automática de proxies.

Um 429 persistente exige reduzir a frequência das consultas e aguardar a
liberação do IP.

### Persistência

O relatório principal passa a ser salvo em:

```text
1_src/keyword_research_app/data/keyword_trends_report.json
```

Uma cópia continua sendo publicada em `web/data/keywords_report.json` para a
interface web.

## Como executar

1. Instale e sincronize as dependências:

   ```powershell
   uv sync
   ```

2. Crie `1_src/keyword_research_app/.env` com:

   ```dotenv
   DATA_SOURCE=GOOGLE_TRENDS
   GOOGLE_TRENDS_LANGUAGE=pt-BR
   GOOGLE_TRENDS_TIMEZONE=180
   GOOGLE_TRENDS_GEO=BR
   GOOGLE_TRENDS_TIMEFRAME=today 3-m
   GOOGLE_TRENDS_MAX_RETRIES=3
   GOOGLE_TRENDS_BACKOFF_SECONDS=5
   GOOGLE_TRENDS_MIN_DELAY_SECONDS=5
   GOOGLE_TRENDS_MAX_DELAY_SECONDS=20
   GOOGLE_TRENDS_CACHE_TTL_HOURS=24
   ```

3. Coloque os termos em `data/input_keywords.json`.

4. Execute na raiz do repositório:

   ```powershell
   uv run python -m keyword_research_app.main
   ```

5. Confira `data/keyword_trends_report.json`.

## Plano de ação

### Etapa 1 — integração mínima

1. Declarar e instalar `pytrends`.
2. Configurar `DATA_SOURCE=GOOGLE_TRENDS`.
3. Consultar cada termo individualmente e sem modificadores.
4. Persistir a série temporal e as métricas derivadas.
5. Exibir erros remotos sem substituir silenciosamente os dados por mock.

Esta etapa foi implementada.

### Etapa 2 — validação funcional

1. Executar consultas pequenas manualmente.
2. Comparar os gráficos retornados com a interface pública do Google Trends.
3. Confirmar idioma, região, fuso e período usados pela análise.
4. Registrar horários e frequência de eventuais respostas 429.
5. Ajustar o backoff conforme o comportamento observado.

### Etapa 3 — confiabilidade

1. Revisar periodicamente a validade configurada para o cache local.
2. Monitorar a quantidade de consultas que reutilizam resultados recentes.
3. Criar testes com respostas simuladas, sem acessar o Google.
4. Registrar logs estruturados sem armazenar cookies ou dados sensíveis.
5. Monitorar alterações de contrato do Google Trends.

### Etapa 4 — evolução da fonte

O repositório oficial do `pytrends` está arquivado e se descreve como uma
“pseudo API”. A última atualização de código registrada no GitHub ocorreu em
2024. Isso aumenta o risco de uma mudança no Google quebrar a integração sem
uma correção oficial da biblioteca.

Para uso crítico, deve-se avaliar a API oficial do Google Trends quando houver
acesso disponível, ou um provedor mantido com contrato e limites documentados.

## Limitações dos dados

- Interesse 100 significa o maior interesse relativo da consulta, não cem
  buscas.
- Os valores dependem dos outros termos comparados, região e período.
- `relevance_score` resume a curva individual; não mede intenção comercial,
  dificuldade de SEO ou conversão.
- Consultas separadas possuem escalas próprias e não representam volume absoluto
  de buscas entre palavras diferentes.
- `pytrends` depende de endpoints não oficiais e pode parar de funcionar.

## Referências

- [Repositório oficial do pytrends](https://github.com/GeneralMills/pytrends)
- [Pacote pytrends no PyPI](https://pypi.org/project/pytrends/)
- [Como os dados do Google Trends são ajustados](https://support.google.com/trends/answer/4365533)
