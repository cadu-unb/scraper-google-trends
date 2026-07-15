# Variáveis e configurações

## Variáveis do n8n

No `docker-compose.yml`, o serviço usa:

```yaml
N8N_BASIC_AUTH_ACTIVE=true
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin
N8N_HOST=localhost
N8N_PORT=5678
N8N_PROTOCOL=http
NODE_ENV=production
N8N_SECURE_COOKIE=false
```

Essas variáveis controlam acesso, host, porta e modo de execução do n8n.

## Variáveis do keyword research

O app Python carrega variáveis em `1_src/keyword_research_app/config/settings.py`.

Principais variáveis:

- `DATA_SOURCE`: fonte de dados. O padrão é `GOOGLE_TRENDS`.
- `GOOGLE_TRENDS_LANGUAGE`: idioma. O padrão é `pt-BR`.
- `GOOGLE_TRENDS_TIMEZONE`: fuso usado pelo Google Trends. O padrão é `180`.
- `GOOGLE_TRENDS_GEO`: região. O padrão é `BR`.
- `GOOGLE_TRENDS_TIMEFRAME`: período. O padrão é `today 12-m`.
- `GOOGLE_TRENDS_MIN_DELAY_SECONDS`: espera mínima entre consultas. O padrão é `5`.
- `GOOGLE_TRENDS_MAX_DELAY_SECONDS`: espera máxima entre consultas. O padrão é `20`.
- `GOOGLE_TRENDS_NEW_QUERY`: controla se o cache será apagado antes da execução.

## Como passar variável no Execute Command

Use a variável antes do comando:

```bash
cd /workspace/1_src && GOOGLE_TRENDS_NEW_QUERY=false python3 -m keyword_research_app.main
```

Também é possível passar mais de uma:

```bash
cd /workspace/1_src && DATA_SOURCE=GOOGLE_TRENDS GOOGLE_TRENDS_NEW_QUERY=false python3 -m keyword_research_app.main
```

## Configuração por arquivo `.env`

O app Python tenta carregar `.env` dentro da pasta:

```text
1_src/keyword_research_app/.env
```

Não foi identificado automaticamente um arquivo `.env.example` para essa aplicação. Se criar um `.env`, não inclua segredos reais em documentação pública.

## O que mudar com segurança

Pode ajustar com cuidado:

- lista em `data/input_keywords.json`;
- delays do Google Trends;
- região `GOOGLE_TRENDS_GEO`;
- período `GOOGLE_TRENDS_TIMEFRAME`;
- variável `GOOGLE_TRENDS_NEW_QUERY`.

Evite mudar sem entender impacto:

- caminho `/workspace/1_src` no Docker;
- nome do módulo `keyword_research_app.main`;
- volume `n8n_data`;
- credenciais reais em arquivos versionados.

