from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ItemLista(Base):
    __tablename__ = "itenslistas"

    lista_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("listas.id"), primary_key=True
    )
    item_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("itens.id"), primary_key=True
    )
    preco: Mapped[str | None] = mapped_column(String(100), nullable=True)

    item: Mapped["ItemModel"] = relationship(
        "ItemModel", back_populates="listas", uselist=False
    )
    lista: Mapped["ListaModel"] = relationship(
        "ListaModel", back_populates="itens", uselist=False
    )
