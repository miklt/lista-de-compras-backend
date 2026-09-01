# lista-de-compras-backend

API REST para gerenciamento de listas de compras, construida com FastAPI e Python 3.14.

## Tech Stack

| Componente      | Tecnologia                    |
| --------------- | ----------------------------- |
| Framework       | FastAPI                       |
| Banco de dados  | PostgreSQL 17                 |
| ORM             | SQLAlchemy 2.0                |
| Validacao       | Pydantic v2                   |
| Container       | Docker + Docker Compose       |
| CI/CD           | GitHub Actions                |
| Testes          | pytest + pytest-cov           |
| Lint            | ruff                          |

## Estrutura do Projeto

```
app/
  main.py              # Entrada da aplicacao FastAPI
  config.py            # Configuracoes via variaveis de ambiente
  database.py          # Conexao com o banco de dados
  models/              # Modelos SQLAlchemy 2.0
    item.py
    item_lista.py
    lista.py
    usuario.py
  schemas/             # Schemas Pydantic (request/response)
    item.py
    item_lista.py
    lista.py
    usuario.py
  routes/              # Endpoints da API
    item.py
    lista.py
    usuario.py
    listagens.py
tests/
  test_api.py          # Testes automatizados com cobertura
docker-compose.yml                 # Producao
docker-compose.homologacao.yml     # Homologacao
Dockerfile                         # Imagem Python 3.14
.github/workflows/ci-cd.yml        # Pipeline CI/CD
```

## Endpoints

| Metodo   | URL                    | Descricao                  |
| -------- | ---------------------- | -------------------------- |
| `GET`    | `/health`              | Health check               |
| `GET`    | `/docs`                | Documentacao Swagger       |
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

---

## Ambientes

### Homologacao

Instancia isolada para testes antes de ir para producao.

| Recurso  | Producao         | Homologacao         |
| -------- | ---------------- | ------------------- |
| API      | `:8000`          | `:8001`             |
| Postgres | `:5432`          | `:5433`             |
| Database | `lista_compras`  | `lista_compras_hml` |
| DEBUG    | `false`          | `true`              |

### Producao

| Recurso  | Producao         |
| -------- | ---------------- |
| API      | `:8000`          |
| Postgres | `:5432`          |
| Database | `lista_compras`  |
| DEBUG    | `false`          |

---

## Executando Localmente

### Com Docker (recomendado)

```bash
cp .env.example .env
docker compose up --build
```

API: `http://localhost:8000` | Docs: `http://localhost:8000/docs`

### Homologacao com Docker

```bash
cp .env.example .env
docker compose -f docker-compose.homologacao.yml up --build
```

API: `http://localhost:8001` | Docs: `http://localhost:8001/docs`

### Sem Docker

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
# Ajuste DATABASE_URL no .env para PostgreSQL local
uvicorn app.main:app --reload
```

---

## Testes

### Executar testes

```bash
source .venv/bin/activate
pytest tests/ -v
```

### Testes com cobertura

```bash
pytest tests/ -v --cov=app --cov-report=term-missing
```

Saida esperada:

```
TOTAL    238      6    97%
Required test coverage of 70.0% reached. Total coverage: 97.48%
======================== 19 passed in 0.96s =========================
```

### Gerar relatorio HTML

```bash
pytest tests/ -v --cov=app --cov-report=html
# Abra htmlcov/index.html no navegador
```

### Cobertura minima

Configurada em `pyproject.toml`:

```toml
[tool.coverage.report]
fail_under = 70
```

O pipeline CI falha se a cobertura cair abaixo de 70%.

---

## Pipeline CI/CD

`.github/workflows/ci-cd.yml` executa 4 estagios:

```
test ──> build-and-push ──> deploy-homologacao ──> deploy-producao
```

| Estagio                | O que faz                                                        |
| ---------------------- | ---------------------------------------------------------------- |
| **test**               | ruff lint + pytest com cobertura (PostgreSQL service container)  |
| **build-and-push**     | Build imagem Docker e push para GitHub Container Registry (GHCR) |
| **deploy-homologacao** | Deploy via SSH + healthcheck em `:8001`                          |
| **deploy-producao**    | Deploy via SSH + healthcheck em `:8000` (requer approval)        |

### Triggers

- `push` na branch `main`: executa todo o pipeline (test -> build -> homologacao -> producao)
- `pull_request` para `main`: executa apenas testes

### Deploy manual de homologacao

```bash
# No servidor, pos push no main:
docker compose -f docker-compose.homologacao.yml pull
docker compose -f docker-compose.homologacao.yml up -d
```

### Deploy manual de producao

```bash
docker compose pull
docker compose up -d
```

---

## Secrets necessarios no GitHub

### Homologacao

| Secret            | Descricao                         |
| ----------------- | --------------------------------- |
| `DEPLOY_HOST`     | IP/hostname do servidor           |
| `DEPLOY_USER`     | Usuario SSH do servidor           |
| `DEPLOY_KEY`      | Chave SSH privada                 |
| `DEPLOY_PORT`     | Porta SSH (default: 22)           |
| `DEPLOY_PATH`     | Caminho do projeto no servidor    |

### Producao

| Secret               | Descricao                           |
| -------------------- | ----------------------------------- |
| `DEPLOY_PROD_HOST`   | IP/hostname do servidor producao    |
| `DEPLOY_PROD_USER`   | Usuario SSH do servidor             |
| `DEPLOY_PROD_KEY`    | Chave SSH privada                   |
| `DEPLOY_PROD_PORT`   | Porta SSH (default: 22)             |
| `DEPLOY_PROD_PATH`   | Caminho do projeto no servidor      |

### Configuracao do Environment no GitHub

Para proteger o deploy de producao com approval manual:

1. Va em **Settings > Environments** no repositorio GitHub
2. Crie um environment chamado `producao`
3. Ative **Required reviewers** e adicione quem pode aprovar

---

## Variaveis de Ambiente

| Variavel           | Padrao                                  | Descricao                |
| ------------------ | --------------------------------------- | ------------------------ |
| `DATABASE_URL`     | `sqlite:///./banco.db`                  | URL de conexao do banco  |
| `SECRET_KEY`       | `change-me-in-production`               | Chave da aplicacao       |
| `DEBUG`            | `false`                                 | Modo debug               |
| `POSTGRES_USER`    | `lista_user`                            | Usuario PostgreSQL       |
| `POSTGRES_PASSWORD`| `lista_pass`                            | Senha PostgreSQL         |
| `POSTGRES_DB`      | `lista_compras`                         | Nome do banco            |

---

## Licenca

MIT
