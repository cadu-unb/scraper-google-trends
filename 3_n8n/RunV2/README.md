### `README.md`

# n8n com Python (via Docker Compose)

Este projeto configura e executa uma instância do **n8n** integrada com **Python 3** e **pipx**, permitindo a execução de scripts Python e automações personalizadas diretamente de dentro dos seus fluxos do n8n.

---

## 🛠️ Pré-requisitos

Certifique-se de que o diretório do seu projeto contém a seguinte estrutura de arquivos:
* `docker-compose.yml`
* `Dockerfile.txt` (que define a instalação do Python sobre a imagem oficial do n8n)
* Pasta `scripts/` (opcional, para mapear seus scripts locais dentro do container)

> **Nota:** Certifique-se de que a propriedade `dockerfile` dentro de `services.n8n.build` no seu `docker-compose.yml` está apontando exatamente para `Dockerfile.txt`.

---

## 🛑 Passo 1: Parar e limpar serviços existentes

Se você já possui serviços rodando nesta pasta (ou quer garantir que tudo seja limpo antes de subir a nova versão), execute o comando abaixo. 

Este comando **para os containers**, **remove-os** e **limpa as redes** criadas para o projeto, sem apagar os seus dados salvos no volume:

```bash
    docker compose down
```

### 🧹 Limpeza pesada (Opcional)

Se você quiser apagar absolutamente tudo (incluindo o banco de dados local do n8n e recomeçar do zero total), adicione a flag `-v` para remover os volumes:

```bash
    # CUIDADO: Isso apagará todos os fluxos e credenciais salvos no n8n do container!
docker stop runv2-n8n
docker rm runv2-n8n
```

---

## 🚀 Passo 2: Construir e subir o serviço

Como estamos utilizando um arquivo `Dockerfile.txt` customizado para injetar o Python dentro do container do n8n, precisamos forçar o Docker a **construir (build)** a imagem antes de rodá-la.

Para construir a imagem e iniciar o serviço em segundo plano (background), execute:

```bash
docker compose up --build -d
```

### O que este comando faz?

* `--build`: Força o Docker a ler o seu `Dockerfile.txt` e compilar a imagem do n8n com Python instalado.
* `-d` (Detached mode): Roda os containers em segundo plano, liberando o seu terminal para uso.

---

## 📈 Comandos Úteis de Monitoramento

Após subir o serviço, você pode gerenciar e monitorar o container com os comandos abaixo:

### Verificar se o container está rodando:

```bash
docker compose ps
```

### Monitorar os logs em tempo real (útil para debug):

```bash
docker compose logs -f
```

---

## 🔓 Acesso ao Painel

Assim que o container iniciar, o n8n estará disponível no seu navegador em:

* **URL:** `http://localhost:5678`
* **Usuário:** `admin` (conforme configurado no `.yml`)
* **Senha:** `admin` (conforme configurado no `.yml`)
```