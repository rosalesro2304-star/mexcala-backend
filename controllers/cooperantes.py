from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from database import get_db
from models.models import Cooperante

# Creamos un "Router" que agrupará todas las rutas relacionadas con los ciudadanos
router = APIRouter(prefix="/cooperantes", tags=["Cooperantes"])

@router.post("/", response_model=Cooperante)
def crear_cooperante(cooperante: Cooperante, db: Session = Depends(get_db)):
    """Registra un nuevo cooperante en Mexcala (inicia automáticamente con deuda de $2000)"""
    db.add(cooperante)
    db.commit()            # Guarda los cambios físicamente en PostgreSQL
    db.refresh(cooperante) # Actualiza el objeto en Python con el ID que le dio la BD
    return cooperante

@router.get("/", response_model=list[Cooperante])
def obtener_cooperantes(db: Session = Depends(get_db)):
    """Obtiene la lista de todos los cooperantes y sus deudas actuales"""
    cooperantes = db.exec(select(Cooperante)).all()
    return cooperantes