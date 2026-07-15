# Como rodar o keyword research pelo n8n

## O que será executado

O n8n deve chamar este módulo Python:

```text
1_src/keyword_research_app/main.py
```

Dentro do container, esse arquivo aparece em:

```text
/workspace/1_src/keyword_research_app/main.py
```

## Comando recomendado no Execute Command

Use este comando no node `Execute Command`:

```bash
cd /workspace/1_src && GOOGLE_TRENDS_NEW_QUERY=false python3 -m keyword_research_app.main
```

## Por que usar `GOOGLE_TRENDS_NEW_QUERY=false`

Essa variável diz para o script preservar o cache.

Preservar cache ajuda a:

- evitar repetir consultas;
- reduzir chance de bloqueio por excesso de requisições;
- continuar uma execução anterior;
- deixar loops mais estáveis.

## Quando usar consulta nova

Use somente quando quiser apagar o cache e consultar tudo novamente:

```bash
cd /workspace/1_src && GOOGLE_TRENDS_NEW_QUERY=true python3 -m keyword_research_app.main
```

## Entrada de dados

As palavras-chave ficam em:

```text
1_src/keyword_research_app/data/input_keywords.json
```

Formato esperado:

```json
{
  "keywords": [
    "curso de ia",
    "ia generativa",
    "letramento digital"
  ]
}
```

## Saídas geradas

Depois da execução, o script gera ou atualiza:

```text
1_src/keyword_research_app/data/keyword_trends_report.json
```

E também:

```text
1_src/keyword_research_app/web/data/keywords_report.json
```

## Fluxo interno do script

1. `main.py` chama `generate_keyword_research_report()`.
2. A função carrega configurações com `load_settings()`.
3. O script lê `data/input_keywords.json`.
4. As palavras-chave são normalizadas.
5. A fonte de dados é escolhida por `DATA_SOURCE`.
6. Para `GOOGLE_TRENDS`, o script consulta dados usando `pytrends`.
7. O relatório é montado.
8. O JSON final é salvo na pasta `data` e copiado para a pasta `web/data`.

## Teste manual dentro do container

Se precisar testar sem criar workflow, entre no container:

```bash
docker compose exec n8n sh
```

Depois rode:

```bash
cd /workspace/1_src
GOOGLE_TRENDS_NEW_QUERY=false python3 -m keyword_research_app.main
```

