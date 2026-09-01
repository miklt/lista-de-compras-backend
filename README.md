# lista-de-compras-backend

API REST para gerenciamento de listas de compras, construida com FastAPI e Python 3.14.

## Tech Stack

- **Framework:** FastAPI
- **Banco de dados:** PostgreSQL 17
- **ORM:** SQLAlchemy 2.0
- **Validacao:** Pydantic v2
- **Container:** Docker + Docker Compose

## Estrutura do Projeto

```
app/
  main.py          # Entrada da aplicacao FastAPI
  config.py        # Configuracoes via variaveis de ambiente
  database.py      # Conexao com o banco de dados
  models/          # Modelos SQLAlchemy
  schemas/         # Schemas Pydantic (request/response)
  routes/          # Endpoints da API
tests/             # Testes automatizados
```

## Endpoints

| Metodo   | URL                    | Descricao                  |
| -------- | ---------------------- | -------------------------- |
| `GET`    | `/health`              | Health check               |
| `POST`   | `/item`                | Criar item                 |
| `GET`    | `/item/{nome}`         | Buscar item por nome       |
| `DELETE` | `/item/{nome}`         | Deletar item               |
| `GET`    | `/itens`               | Listar todos os itens      |
| `POST`   | `/usuario`             | Criar usuario              |
| `GET`    | `/usuario/{nome}`      | Buscar usuario por nome    |
| `GET`    | `/usuarios`            | Listar todos os usuarios   |
| `POST`   | `/lista`               | Criar lista de compras     |
| `GET`    | `/lista/{nome}`        | Buscar lista por nome      |
| `GET`    | `/listas`              | Listar todas as listas     |

## Executando Localmente

### Com Docker (recomendado)

```bash
# Copie o arquivo de variaveis de ambiente
cp .env.example .env

# Suba os containers
docker compose up --build
```

A API estara disponivel em `http://localhost:8000` e a documentacao interativa em `http://localhost:8000/docs`.

### Sem Docker

```bash
# Crie um ambiente virtual
python3 -m venv .venv
source .venv/bin/activate

# Instale as dependencias
pip install -r requirements.txt

# Configure o banco (ajuste DATABASE_URL no .env para PostgreSQL)
cp .env.example .env

# Execute
uvicorn app.main:app --reload
```

## Testes

```bash
source .venv/bin/activate
pip install pytest httpx
pytest tests/ -v
```

## Deploy

O projeto possui um pipeline GitHub Actions (`.github/workflows/ci-cd.yml`) que:

1. **Testa** o codigo (lint + testes com PostgreSQL)
2. **Builda** a imagem Docker e pusha para o GitHub Container Registry
3. **Faz deploy** via SSH no servidor de destino

### Secrets necessarios no GitHub

| Secret            | Descricao                         |
| ----------------- | --------------------------------- |
| `DEPLOY_HOST`     | IP/hostname do servidor           |
| `DEPLOY_USER`     | Usuario SSH do servidor           |
| `DEPLOY_KEY`      | Chave SSH privada                 |
| `DEPLOY_PORT`     | Porta SSH (default: 22)           |
| `DEPLOY_PATH`     | Caminho do projeto no servidor    |

### No servidor de destino

```bash
# Instale o Docker e Docker Compose, depois clone o repo e execute:
docker compose pull
docker compose up -d
```

## Licenca

MIT
