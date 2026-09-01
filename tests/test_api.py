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


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_criar_item():
    response = client.post("/item", json={"nome": "tomate"})
    assert response.status_code == 201
    data = response.json()
    assert data["nome"] == "tomate"
    assert "id" in data


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


def test_listar_itens():
    response = client.get("/itens")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_criar_usuario():
    response = client.post(
        "/usuario", json={"nome": "teste", "email": "teste@email.com"}
    )
    assert response.status_code == 201
    assert response.json()["nome"] == "teste"


def test_listar_usuarios():
    response = client.get("/usuarios")
    assert response.status_code == 200
