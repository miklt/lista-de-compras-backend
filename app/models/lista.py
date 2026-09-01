from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ListaModel(Base):
    __tablename__ = "listas"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), unique=True)
    usuario_id: Mapped[int] = mapped_column(Integer, ForeignKey("usuarios.id"))
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    usuario: Mapped["UsuarioModel"] = relationship(
        "UsuarioModel", back_populates="listas"
    )
    itens: Mapped[list["ItemLista"]] = relationship(
        "ItemLista", back_populates="lista"
    )
