from pydantic import BaseModel, ConfigDict

from app.schemas.item import ItemResponse


class ItemListaBase(BaseModel):
    preco: str | None = None


class ItemListaCreate(ItemListaBase):
    nome: str


class ItemListaResponse(ItemListaBase):
    model_config = ConfigDict(from_attributes=True)

    item: ItemResponse
