# Como funciona o Docker deste n8n

## Arquivos envolvidos

- `3_n8n/RunV2/docker-compose.yml`
- `3_n8n/RunV2/dockerfile-n8n-python`

## O que o compose faz

O `docker-compose.yml` cria um serviço chamado `n8n`.

Ele expõe a porta:

```text
5678:5678
```

Isso significa:

- porta `5678` na sua máquina;
- porta `5678` dentro do container.

Por isso o painel abre em:

```text
http://localhost:5678
```

## Volumes configurados

O compose usa três montagens importantes:

```yaml
- n8n_data:/home/node/.n8n
- ./scripts:/scripts
- ../../1_src:/workspace/1_src
```

O que cada uma faz:

- `n8n_data:/home/node/.n8n`: guarda dados internos do n8n.
- `./scripts:/scripts`: permite colocar scripts locais em `3_n8n/RunV2/scripts`.
- `../../1_src:/workspace/1_src`: deixa a pasta `1_src` disponível dentro do container.

## Por que `/workspace/1_src` importa?

Dentro do container, o script Python deve ser chamado a partir de `/workspace/1_src`.

Comando recomendado:

```bash
cd /workspace/1_src && GOOGLE_TRENDS_NEW_QUERY=false python3 -m keyword_research_app.main
```

Se você chamar o Python de outro lugar, ele pode não encontrar o módulo `keyword_research_app`.

## O que o Dockerfile faz

O `dockerfile-n8n-python` parte da imagem oficial:

```dockerfile
FROM n8nio/n8n:2.29.1
```

Depois ele copia Python 3.11 de uma imagem Alpine e instala:

- `pipx`
- dependências de `1_src/keyword_research_app/requirements.txt`

As dependências atuais do scraper são:

- `python-dotenv`
- `pytrends`

## Quando reconstruir a imagem

Reconstrua com `--build` quando:

- mudar `dockerfile-n8n-python`;
- mudar `requirements.txt`;
- adicionar dependências Python necessárias ao n8n;
- trocar a versão base do n8n.

