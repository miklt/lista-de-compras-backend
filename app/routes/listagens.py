from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.item import ItemModel
from app.models.lista import ListaModel
from app.models.usuario import UsuarioModel
from app.schemas.item import ItemResponse
from app.schemas.lista import ListaResponse
from app.schemas.usuario import UsuarioResponse

router = APIRouter(tags=["listagens"])


@router.get("/itens", response_model=list[ItemResponse])
def listar_itens(db: Session = Depends(get_db)):
    return db.query(ItemModel).all()


@router.get("/listas", response_model=list[ListaResponse])
def listar_listas(db: Session = Depends(get_db)):
    return db.query(ListaModel).all()


@router.get("/usuarios", response_model=list[UsuarioResponse])
def listar_usuarios(db: Session = Depends(get_db)):
    return db.query(UsuarioModel).all()
