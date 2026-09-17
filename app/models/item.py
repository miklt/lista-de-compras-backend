from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ItemModel(Base):
    __tablename__ = "itens"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), unique=True)
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    listas: Mapped[list["ItemLista"]] = relationship(
        "ItemLista", back_populates="item"
    )
