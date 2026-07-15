# Erros comuns

## `python3: not found`

Possível causa:

- A imagem antiga do n8n está rodando sem o Dockerfile com Python.

Como resolver:

```bash
cd 3_n8n/RunV2
docker compose up --build -d
```

## `No module named keyword_research_app`

Possível causa:

- O comando foi executado fora de `/workspace/1_src`.

Use:

```bash
cd /workspace/1_src && GOOGLE_TRENDS_NEW_QUERY=false python3 -m keyword_research_app.main
```

## `No such file or directory`

Possíveis causas:

- O volume `../../1_src:/workspace/1_src` não foi montado.
- O comando foi rodado fora do container esperado.
- O `docker compose` foi executado em outra pasta.

Verifique a configuração:

```bash
cd 3_n8n/RunV2
docker compose config
```

## Dependência Python não encontrada

Possível causa:

- `requirements.txt` mudou, mas a imagem não foi reconstruída.

Como resolver:

```bash
cd 3_n8n/RunV2
docker compose up --build -d
```

## `ImportError: Error loading shared library libffi.so.8`

Possível causa:

- O Python importou `pandas`, `pytrends` ou `_ctypes`, mas a imagem Alpine do
  n8n não tinha a biblioteca nativa `libffi`.

Como resolver:

1. Confirme que o `dockerfile-n8n-python` copia `libffi` da imagem Python:

```dockerfile
COPY --from=python-base /usr/lib/libffi.so.8* /usr/lib/
```

2. Reconstrua a imagem:

```bash
cd 3_n8n/RunV2
docker compose up --build -d
```

3. Rode novamente o comando no n8n:

```bash
cd /workspace/1_src && GOOGLE_TRENDS_NEW_QUERY=false python3 -m keyword_research_app.main
```

## `PermissionError: Permission denied: google_trends_cache.json.tmp`

Possível causa:

- O n8n roda dentro do container como usuário `node`, normalmente UID `1000`.
- A pasta montada do projeto pode aparecer dentro do container com outro dono,
  por exemplo UID `1001`.
- Com isso, o script lê os arquivos, mas não consegue criar cache e relatórios.

Como conferir:

```bash
cd 3_n8n/RunV2
docker compose exec n8n id
docker compose exec n8n sh -lc "ls -ldn /workspace/1_src/keyword_research_app/data"
```

Como resolver neste projeto:

```bash
chmod 777 1_src/keyword_research_app/data 1_src/keyword_research_app/web/data
chmod 666 1_src/keyword_research_app/web/data/keywords_report.json
```

Depois teste a escrita:

```bash
cd 3_n8n/RunV2
docker compose exec n8n sh -lc "touch /workspace/1_src/keyword_research_app/data/.n8n-write-test && rm /workspace/1_src/keyword_research_app/data/.n8n-write-test"
```

## O workflow fica demorando muito

Possíveis causas:

- Muitas palavras-chave em `input_keywords.json`.
- Delay configurado entre consultas.
- Google Trends respondendo lentamente.

Isso pode ser esperado. O próprio app estima tempo médio com base nos delays.

## Google Trends falha ou bloqueia

Possíveis causas:

- Muitas consultas em sequência.
- Cache apagado com frequência.
- Loop executando em intervalo curto.

Medidas práticas:

- use `GOOGLE_TRENDS_NEW_QUERY=false`;
- reduza a lista de palavras-chave;
- aumente o intervalo do Schedule;
- rode testes manuais antes de automatizar.

## Login do n8n não funciona

As credenciais configuradas são:

- Usuário: `admin`
- Senha: `admin`

Se você alterou o `docker-compose.yml`, confira:

```yaml
N8N_BASIC_AUTH_USER=admin
N8N_BASIC_AUTH_PASSWORD=admin
```

## Alterei o compose, mas nada mudou

Possível causa:

- O container antigo ainda está rodando.

Tente:

```bash
cd 3_n8n/RunV2
docker compose down
docker compose up --build -d
```
