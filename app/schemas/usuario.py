from datetime import datetime

from pydantic import BaseModel, ConfigDict


class UsuarioBase(BaseModel):
    nome: str
    email: str


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioResponse(UsuarioBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    data_cadastro: datetime


class UsuarioSimplificado(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    nome: str
