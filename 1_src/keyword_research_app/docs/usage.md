# Como usar a aplicacao

## 1. Instalar dependencias

Entre na pasta do app:

```bash
cd 1_src/keyword_research_app
```

Instale as dependencias:

```bash
pip install -r requirements.txt
```

## 2. Configurar variaveis

Crie um arquivo `.env` a partir do exemplo:

```bash
cp .env.example .env
```

Para usar a versao simulada, mantenha:

```env
DATA_SOURCE=GOOGLE_TRENDS
GOOGLE_TRENDS_LANGUAGE=pt-BR
GOOGLE_TRENDS_TIMEZONE=180
GOOGLE_TRENDS_GEO=BR
GOOGLE_TRENDS_TIMEFRAME=today 3-m
GOOGLE_TRENDS_MIN_DELAY_SECONDS=5
GOOGLE_TRENDS_MAX_DELAY_SECONDS=20
```

## 3. Editar entrada JSON

Edite `data/input_keywords.json`:

```json
{
  "keywords": [
    "curso de ia",
    "ia generativa",
    "letramento digital"
  ]
}
```

A chave `keywords` e obrigatoria e deve conter uma lista de strings.

## 4. Executar o Python

Rode:

```bash
uv run python -m keyword_research_app.main
```

Ao final, a aplicacao cria:

- `data/keyword_trends_report.json`
- `web/data/keywords_report.json`

## 5. Abrir a web app

Abra `web/index.html` no navegador.

Se o navegador bloquear a leitura do JSON local, entre na pasta `web` e rode:

```bash
python -m http.server 8000
```

Depois acesse `http://localhost:8000`.

## 6. Fluxo interno

1. `generate_keyword_research_report()` carrega as configuracoes.
2. `app/input_loader.py` le e valida o JSON de entrada.
3. `app/normalizer.py` normaliza textos e preserva a ordem original.
4. `integrations/mock_client.py` gera metricas simuladas.
5. `app/report_builder.py` calcula crescimento e relevancia.
6. `app/json_exporter.py` gera `metadata`, `columns` e `rows`.
7. `web/js/app.js` le o JSON e monta a tabela dinamicamente.
