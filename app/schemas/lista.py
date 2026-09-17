from datetime import datetime

from pydantic import BaseModel, ConfigDict

from app.schemas.item_lista import ItemListaCreate, ItemListaResponse
from app.schemas.usuario import UsuarioSimplificado


class ListaBase(BaseModel):
    nome: str


class ListaCreate(ListaBase):
    itens: list[ItemListaCreate]


class ListaResponse(ListaBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    data_cadastro: datetime
    itens: list[ItemListaResponse]
    usuario: UsuarioSimplificado
