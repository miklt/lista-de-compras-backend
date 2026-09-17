from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class UsuarioModel(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    nome: Mapped[str] = mapped_column(String(200), unique=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime, default=lambda: datetime.now(timezone.utc)
    )

    listas: Mapped[list["ListaModel"]] = relationship(
        "ListaModel", back_populates="usuario"
    )
