# Documentacao for dummies

## O que e este projeto?

Este projeto e uma aplicacao Python para transformar um arquivo JSON de palavras-chave em outro JSON de analise. Uma pagina HTML usa esse JSON para mostrar uma tabela interativa no navegador. A versao atual usa dados simulados, entao voce consegue testar tudo sem conta Google e sem credenciais.

## O que voce consegue fazer com ele?

- Rodar um arquivo JSON de palavras-chave.
- Gerar `data/keyword_trends_report.json`.
- Abrir uma tabela no navegador.
- Pesquisar e ordenar dados da tabela.
- Entender onde conectar Google Ads API futuramente.

## Antes de comecar

Voce precisa ter Python 3.11 ou superior instalado.

As dependencias ficam em `requirements.txt`. Dependencias sao bibliotecas que o projeto usa para trabalhar com tabelas, Excel e variaveis de ambiente.

## Como iniciar do zero

Entre na pasta:

```bash
cd 1_src/keyword_research_app
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

Execute:

```bash
uv run python -m keyword_research_app.main
```

Abra `web/index.html` no navegador.

## Como saber se funcionou?

Funcionou quando o terminal disser que o JSON foi gerado e estes arquivos existirem:

- `data/keyword_trends_report.json`
- `web/data/keywords_report.json`

## Problemas comuns

Se aparecer erro dizendo que `dotenv` nao existe, instale as dependencias com:

```bash
pip install -r requirements.txt
```

Se a fonte `GOOGLE_ADS` nao retornar dados reais, isso e esperado nesta versao. A aplicacao ainda nao implementa a chamada oficial.

## Glossario rapido

- Palavra-chave: termo que uma pessoa pesquisaria no Google.
- CSV: tabela em texto, facil de abrir em Excel ou importar em sistemas.
- XLSX: arquivo do Excel.
- JSON: arquivo de texto estruturado usado para trocar dados entre Python e JavaScript.
- Mock: dado simulado para testar o sistema sem depender de servicos externos.
- Google Ads Keyword Planner: ferramenta mais adequada para volume e competicao de buscas.
- Google Trends: ferramenta para interesse relativo ao longo do tempo.

## Encadeamento de funcoes

1. O usuario executa o modulo `keyword_research_app.main`.
2. `generate_keyword_research_report()` chama `load_settings()`.
3. `load_keywords_from_json()` le `data/input_keywords.json`.
4. `normalize_keywords()` limpa os termos e remove duplicatas.
5. `fetch_keyword_metrics_by_source()` escolhe a fonte de dados.
6. `fetch_keyword_metrics()` em `mock_client.py` cria metricas simuladas.
7. `build_keyword_report()` monta a tabela final e calcula relevancia.
8. `export_report_json()` salva o JSON final.
9. `web/js/app.js` le o JSON e constroi a tabela no navegador.
