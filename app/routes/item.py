from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.item import ItemModel
from app.schemas.item import ItemCreate, ItemResponse

router = APIRouter(prefix="/item", tags=["itens"])


@router.get("/{nome}", response_model=ItemResponse)
def buscar_item(nome: str, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.nome == nome).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item '{nome}' nao encontrado")
    return item


@router.post("", response_model=ItemResponse, status_code=201)
def criar_item(data: ItemCreate, db: Session = Depends(get_db)):
    existente = db.query(ItemModel).filter(ItemModel.nome == data.nome).first()
    if existente:
        raise HTTPException(
            status_code=400, detail=f"Item '{data.nome}' ja existe"
        )
    item = ItemModel(nome=data.nome)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


@router.delete("/{nome}", response_model=list[ItemResponse])
def deletar_item(nome: str, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.nome == nome).first()
    if not item:
        raise HTTPException(status_code=404, detail=f"Item '{nome}' nao encontrado")
    db.delete(item)
    db.commit()
    itens = db.query(ItemModel).all()
    return itens
