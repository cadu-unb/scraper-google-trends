# Documentação 

## O que é este projeto?

Esta pasta documenta o serviço n8n que fica em `3_n8n/RunV2`.

O n8n é uma ferramenta visual para automatizar tarefas. Neste projeto, ele roda em Docker e recebeu Python dentro da imagem para conseguir executar scripts do repositório, como `1_src/keyword_research_app/main.py`.

## O que você consegue fazer com ele?

- Subir o painel do n8n em `http://localhost:5678`.
- Criar workflows com agenda, loops e comandos.
- Rodar scripts Python de dentro do container.
- Executar o fluxo de pesquisa de palavras-chave com Google Trends.
- Reaproveitar cache para evitar consultas repetidas.

## Antes de começar

Você precisa ter Docker e Docker Compose funcionando na máquina.

Arquivos principais:

- `3_n8n/RunV2/docker-compose.yml`: define como o serviço n8n sobe.
- `3_n8n/RunV2/dockerfile-n8n-python`: cria a imagem do n8n com Python.
- `1_src/keyword_research_app/main.py`: script Python chamado pelo loop.
- `1_src/keyword_research_app/data/input_keywords.json`: entrada com as palavras-chave.

## Como iniciar do zero

Leia primeiro:

1. [como-subir-o-n8n.md](como-subir-o-n8n.md)
2. [como-criar-loops.md](como-criar-loops.md)
3. [como-rodar-keyword-research.md](como-rodar-keyword-research.md)

## Como saber se funcionou?

O serviço funcionou quando:

- `docker compose ps` mostra o container `n8n` rodando.
- O navegador abre `http://localhost:5678`.
- O login aceita `admin` / `admin`.
- Um workflow com `Execute Command` consegue rodar `python3 --version`.
- O workflow do scraper gera ou atualiza `1_src/keyword_research_app/data/keyword_trends_report.json`.

## Problemas comuns

Veja [erros-comuns.md](erros-comuns.md).

Os problemas mais frequentes são:

- Container não foi reconstruído depois de alterar o Dockerfile.
- O comando foi executado no diretório errado.
- O script Python não encontrou o módulo `keyword_research_app`.
- O Google Trends limitou ou bloqueou consultas repetidas.
- O cache foi apagado sem necessidade.

## Glossário rápido

- Docker: ferramenta que roda aplicações em ambientes isolados chamados containers.
- Container: ambiente onde o n8n roda.
- Compose: arquivo que descreve como subir containers.
- Workflow: automação criada dentro do n8n.
- Node: bloco individual dentro de um workflow.
- Schedule Trigger: node que dispara um workflow em horários definidos.
- Execute Command: node que roda um comando de terminal dentro do container.
- Cache: arquivo que guarda resultados já coletados para evitar repetir consultas.

## Encadeamento de funções

Fluxo básico do loop:

1. O n8n dispara o workflow por horário, manualmente ou por outro gatilho.
2. O node `Execute Command` entra em `/workspace/1_src`.
3. O comando executa `python3 -m keyword_research_app.main`.
4. O Python lê `keyword_research_app/data/input_keywords.json`.
5. O Python carrega configurações em `keyword_research_app/config/settings.py`.
6. O Python consulta a fonte configurada, normalmente `GOOGLE_TRENDS`.
7. O relatório é salvo em `keyword_research_app/data/keyword_trends_report.json`.
8. Uma cópia é enviada para `keyword_research_app/web/data/keywords_report.json`.

