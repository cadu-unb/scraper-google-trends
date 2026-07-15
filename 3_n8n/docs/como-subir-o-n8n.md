# Como subir o n8n

## Onde rodar os comandos

Entre na pasta do serviço:

```bash
cd 3_n8n/RunV2
```

## Subir com rebuild

Use este comando quando for a primeira vez ou quando o Dockerfile mudar:

```bash
docker compose up --build -d
```

O que ele faz:

- `up`: sobe o serviço.
- `--build`: reconstrói a imagem do n8n com Python.
- `-d`: deixa o container rodando em segundo plano.

## Subir sem rebuild

Use quando nada mudou no Dockerfile:

```bash
docker compose up -d
```

## Ver se está rodando

```bash
docker compose ps
```

## Ver logs

```bash
docker compose logs -f
```

## Acessar no navegador

Abra:

```text
http://localhost:5678
```

Credenciais configuradas no `docker-compose.yml`:

- Usuário: `admin`
- Senha: `admin`

## Parar o serviço

```bash
docker compose down
```

Este comando para e remove o container, mas preserva o volume `n8n_data`, onde ficam dados do n8n.

## O que evitar

Evite remover volumes sem ter certeza. Apagar volumes pode remover workflows, credenciais e configurações salvas no n8n.

