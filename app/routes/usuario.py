from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.usuario import UsuarioModel
from app.schemas.usuario import UsuarioCreate, UsuarioResponse

router = APIRouter(prefix="/usuario", tags=["usuarios"])


@router.get("/{nome}", response_model=UsuarioResponse)
def buscar_usuario(nome: str, db: Session = Depends(get_db)):
    usuario = db.query(UsuarioModel).filter(UsuarioModel.nome == nome).first()
    if not usuario:
        raise HTTPException(status_code=404, detail=f"Usuario '{nome}' nao encontrado")
    return usuario


@router.post("", response_model=UsuarioResponse, status_code=201)
def criar_usuario(data: UsuarioCreate, db: Session = Depends(get_db)):
    existente = db.query(UsuarioModel).filter(
        UsuarioModel.nome == data.nome
    ).first()
    if existente:
        raise HTTPException(
            status_code=400, detail="Usuario ja existe"
        )
    usuario = UsuarioModel(nome=data.nome, email=data.email)
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario
