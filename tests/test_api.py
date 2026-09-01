from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_module():
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)
    import os

    os.remove("test.db")


# ── Health ──────────────────────────────────────────────────────────


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


# ── Itens ───────────────────────────────────────────────────────────


def test_criar_item():
    response = client.post("/item", json={"nome": "tomate"})
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "tomate"
    assert "id" in data
    assert "data_criacao" in data


def test_buscar_item():
    client.post("/item", json={"nome": "cebola"})
    response = client.get("/item/cebola")
    assert response.status_code == 200
    assert response.json()["nome"] == "cebola"


def test_item_nao_encontrado():
    response = client.get("/item/inexistente")
    assert response.status_code == 404


def test_item_duplicado():
    client.post("/item", json={"nome": "alho"})
    response = client.post("/item", json={"nome": "alho"})
    assert response.status_code == 400


def test_deletar_item():
    client.post("/item", json={"nome": "pimentao"})
    response = client.delete("/item/pimentao")
    assert response.status_code == 200
    assert not any(i["nome"] == "pimentao" for i in response.json())


def test_deletar_item_inexistente():
    response = client.delete("/item/naoexiste")
    assert response.status_code == 404


def test_listar_itens():
    response = client.get("/itens")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) > 0


# ── Usuarios ────────────────────────────────────────────────────────


def test_criar_usuario():
    response = client.post(
        "/usuario", json={"nome": "teste_user", "email": "teste@email.com"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "teste_user"
    assert data["email"] == "teste@email.com"
    assert "id" in data
    assert "data_cadastro" in data


def test_usuario_duplicado():
    client.post(
        "/usuario", json={"nome": "dup_user", "email": "dup@email.com"}
    )
    response = client.post(
        "/usuario", json={"nome": "dup_user", "email": "dup2@email.com"}
    )
    assert response.status_code == 400


def test_buscar_usuario():
    client.post(
        "/usuario", json={"nome": "busca_user", "email": "busca@email.com"}
    )
    response = client.get("/usuario/busca_user")
    assert response.status_code == 200
    assert response.json()["nome"] == "busca_user"


def test_usuario_nao_encontrado():
    response = client.get("/usuario/naoexiste")
    assert response.status_code == 404


def test_listar_usuarios():
    response = client.get("/usuarios")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ── Listas ──────────────────────────────────────────────────────────


def test_criar_lista():
    client.post("/item", json={"nome": "arroz"})
    client.post("/item", json={"nome": "feijao"})
    response = client.post(
        "/lista",
        json={
            "nome": "Lista Teste",
            "itens": [
                {"nome": "arroz", "preco": "10 reais"},
                {"nome": "feijao", "preco": "8 reais"},
            ],
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "Lista Teste"
    assert len(data["itens"]) == 2


def test_lista_duplicada():
    client.post(
        "/lista",
        json={"nome": "Lista Dup", "itens": [{"nome": "arroz"}]},
    )
    response = client.post(
        "/lista",
        json={"nome": "Lista Dup", "itens": [{"nome": "arroz"}]},
    )
    assert response.status_code == 400


def test_buscar_lista():
    client.post(
        "/lista",
        json={"nome": "Lista Busca", "itens": [{"nome": "arroz"}]},
    )
    response = client.get("/lista/Lista Busca")
    assert response.status_code == 200
    assert response.json()["nome"] == "Lista Busca"
    assert "itens" in response.json()
    assert "usuario" in response.json()


def test_lista_nao_encontrada():
    response = client.get("/lista/naoexiste")
    assert response.status_code == 404


def test_listar_listas():
    response = client.get("/listas")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_criar_lista_item_novo():
    response = client.post(
        "/lista",
        json={
            "nome": "Lista Item Novo",
            "itens": [{"nome": "item_autocriado_test"}],
        },
    )
    assert response.status_code == 201
    assert len(response.json()["itens"]) == 1
