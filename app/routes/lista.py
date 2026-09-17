from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload

from app.database import get_db
from app.models.item import ItemModel
from app.models.item_lista import ItemLista
from app.models.lista import ListaModel
from app.schemas.lista import ListaCreate, ListaResponse

router = APIRouter(prefix="/lista", tags=["listas"])


@router.get("/{nome}", response_model=ListaResponse)
def buscar_lista(nome: str, db: Session = Depends(get_db)):
    lista = (
        db.query(ListaModel)
        .options(joinedload(ListaModel.itens).joinedload(ItemLista.item))
        .options(joinedload(ListaModel.usuario))
        .filter(ListaModel.nome == nome)
        .first()
    )
    if not lista:
        raise HTTPException(status_code=404, detail=f"Lista '{nome}' nao encontrada")
    return lista


@router.post("", response_model=ListaResponse, status_code=201)
def criar_lista(data: ListaCreate, db: Session = Depends(get_db)):
    existente = db.query(ListaModel).filter(ListaModel.nome == data.nome).first()
    if existente:
        raise HTTPException(
            status_code=400, detail="Uma lista ja existe com esse nome"
        )

    lista = ListaModel(nome=data.nome, usuario_id=1)

    for item_data in data.itens:
        item_db = db.query(ItemModel).filter(ItemModel.nome == item_data.nome).first()
        if not item_db:
            item_db = ItemModel(nome=item_data.nome)
            db.add(item_db)
            db.flush()

        il = ItemLista(preco=item_data.preco, item=item_db)
        lista.itens.append(il)

    db.add(lista)
    db.commit()

    lista = (
        db.query(ListaModel)
        .options(joinedload(ListaModel.itens).joinedload(ItemLista.item))
        .options(joinedload(ListaModel.usuario))
        .filter(ListaModel.nome == data.nome)
        .first()
    )
    return lista
