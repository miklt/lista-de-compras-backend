from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ItemBase(BaseModel):
    nome: str


class ItemCreate(ItemBase):
    pass


class ItemResponse(ItemBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_criacao: datetime
