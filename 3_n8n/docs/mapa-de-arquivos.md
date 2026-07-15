# Mapa de arquivos

## Pasta principal

```text
3_n8n/
```

Guarda a configuração do n8n usado neste repositório.

## Serviço atual

```text
3_n8n/RunV2/
```

Contém a versão atual do serviço n8n com Docker Compose.

## Compose

```text
3_n8n/RunV2/docker-compose.yml
```

Define:

- build da imagem;
- porta `5678`;
- variáveis de ambiente do n8n;
- volumes;
- política de restart.

## Dockerfile

```text
3_n8n/RunV2/dockerfile-n8n-python
```

Cria uma imagem do n8n com Python e dependências do scraper.

## Scripts locais

```text
3_n8n/RunV2/scripts/
```

Pasta opcional montada dentro do container em:

```text
/scripts
```

Não foi identificado automaticamente nenhum script dentro dessa pasta.

## Código Python chamado pelo n8n

```text
1_src/keyword_research_app/
```

Dentro do container, essa pasta aparece em:

```text
/workspace/1_src/keyword_research_app/
```

## Arquivo de entrada do scraper

```text
1_src/keyword_research_app/data/input_keywords.json
```

Guarda a lista de palavras-chave.

## Arquivos de saída do scraper

```text
1_src/keyword_research_app/data/keyword_trends_report.json
1_src/keyword_research_app/web/data/keywords_report.json
```

O primeiro é o relatório principal. O segundo é a cópia usada pela mini aplicação web.

