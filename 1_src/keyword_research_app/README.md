# Keyword Research App

Aplicacao Python pequena e modular para analisar palavras-chave e gerar um JSON pronto para visualizacao em uma mini-aplicacao web estatica.

O Python processa os dados. A interface em HTML, CSS e JavaScript apenas consome o JSON mais recente e monta uma tabela interativa.

## O que o projeto faz

- Le palavras-chave exclusivamente de um arquivo JSON.
- Normaliza os termos e preserva a ordem original.
- Coleta interesse relativo com `DATA_SOURCE=GOOGLE_TRENDS`.
- Mantem `DATA_SOURCE=MOCK` apenas para testes locais.
- Consulta cada palavra-chave sem adicionar modificadores.
- Analisa a curva individual de cada termo nos últimos três meses.
- Usa cache e espera aleatória entre consultas ao Google Trends.
- Calcula direção, variação da curva e `relevance_score`.
- Gera `data/keyword_trends_report.json` como saida principal.
- Copia o JSON gerado para `web/data/keywords_report.json`.
- Exibe os dados em uma mini-aplicacao web com busca, filtros e ordenacao.

## O que o projeto nao faz

- Nao e Google Analytics.
- Nao mede visitas, sessoes, eventos ou comportamento dentro de sites.
- Nao faz scraping direto do Google.
- Nao inclui credenciais reais.
- Nao usa React, Vue, Angular ou frameworks externos.
- CSV e XLSX nao sao mais o foco do fluxo principal.

## Por que nao e Google Analytics

Google Analytics mede comportamento dentro de propriedades digitais que voce
controla. Este projeto analisa o interesse relativo e a curva temporal de termos
pesquisados no Google Trends.

## Entrada JSON

A entrada principal fica em `data/input_keywords.json`:

```json
{
  "keywords": [
    "curso de ia",
    "ia generativa",
    "letramento digital",
    "ferramentas de ia",
    "inteligência artificial na educação"
  ]
}
```

O arquivo precisa ter a chave `keywords` com uma lista de strings.

## Saida JSON

Ao executar o Python, estes arquivos sao gerados ou atualizados:

- `data/keyword_trends_report.json`: saida principal.
- `web/data/keywords_report.json`: copia consumida pela mini-aplicacao web.

A estrutura final tem `metadata`, `columns` e `rows`:

```json
{
  "metadata": {
    "generated_at": "2026-06-24T10:30:00",
    "source": "GOOGLE_TRENDS",
    "total_keywords": 5,
    "description": "Keyword research report generated from JSON input."
  },
  "columns": [
    { "key": "keyword", "label": "Palavra-chave" }
  ],
  "rows": [
    {
      "keyword": "curso de ia",
      "average_interest": 42.8,
      "latest_interest": 51,
      "peak_interest": 79,
      "trend_direction": "CRESCENTE",
      "trend_change": 12.4,
      "relevance_score": 49.18,
      "source": "GOOGLE_TRENDS"
    }
  ]
}
```

## Instalar dependencias

Na raiz do repositório, execute:

```bash
uv sync
```

## Executar o processamento Python

Na raiz do repositorio, rode:

```bash
uv run python -m keyword_research_app.main
```

A funcao de negocio executada pelo comando e
`generate_keyword_research_report()`.

Com a configuração padrão, consultas novas aguardam entre 5 e 20 segundos. O
cache em `data/google_trends_cache.json` evita repetir termos coletados nas
últimas 24 horas e permite retomar uma lista longa.

## Converter uma lista para o JSON de entrada

Use `convert_keywords_to_json()` para gravar a entrada aceita pela aplicacao:

```python
from keyword_research_app.utils import convert_keywords_to_json

saved_path = convert_keywords_to_json(["curso de ia", "ia generativa"])
print(saved_path)
```

Sem informar outro caminho, o arquivo e salvo em
`data/input_keywords.json`, substituindo a entrada anterior.

## Abrir a mini-aplicacao web

Abra:

```text
1_src/keyword_research_app/web/index.html
```

A web app tenta carregar primeiro `web/data/keywords_report.json`. Se esse arquivo nao existir, tenta carregar `web/data/keywords_report.example.json`.

Se o navegador bloquear leitura de JSON por causa de abertura direta via `file://`, rode um servidor estatico dentro da pasta `web`:

```bash
python -m http.server 8000
```

Depois abra:

```text
http://localhost:8000
```

## Como funcionam busca e ordenacao

A busca fica acima da tabela e procura em todas as colunas exibidas. Digitar `HIGH`, `MOCK` ou `ia`, por exemplo, filtra qualquer registro que contenha esse texto em algum atributo.

A ordenacao pode ser feita clicando no cabecalho de qualquer coluna ou usando os seletores de coluna e direcao. Textos usam A-Z/Z-A; numeros usam menor-maior/maior-menor.

## Como alterar colunas exibidas

Altere `GOOGLE_TRENDS_REPORT_COLUMNS` em `app/json_exporter.py`. O JavaScript
monta a tabela dinamicamente com base em `columns`.

## Onde alterar estilos visuais

Os estilos ficam em `web/css/styles.css`.

## Onde alterar busca e ordenacao

As regras ficam em `web/js/app.js`, principalmente nas funcoes `applySearch`, `applySorting` e `formatValue`.

## Evoluir para Google Ads API real

O ponto principal para implementar a chamada real fica em `integrations/google_ads_client.py`, na funcao `fetch_keyword_metrics`.

Google Ads Keyword Planner e a fonte mais adequada para volume medio mensal, competicao, indice de competicao e estimativas de lance. Google Trends pode complementar com interesse relativo, mas nao substitui volume absoluto.
