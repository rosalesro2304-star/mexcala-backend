from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from database import get_db
from models.models import Aportacion, Cooperante
from core.factory import AportacionFactory

router = APIRouter(prefix="/aportaciones", tags=["Aportaciones"])

@router.post("/")
def registrar_aportacion(id_cooperante: int, monto: float, db: Session = Depends(get_db)):
    """Registra un pago usando la Factory y actualiza la deuda automáticamente"""
    
    # 1. Buscamos al cooperante en la base de datos (Singleton nos da la conexión 'db')
    cooperante = db.get(Cooperante, id_cooperante)
    if not cooperante:
        raise HTTPException(status_code=404, detail="Cooperante no encontrado")

    # 2. Usamos la Factory para clasificar el pago y crear el objeto
    nueva_aportacion = AportacionFactory.procesar_pago(
        id_cooperante=cooperante.id,
        monto_ingresado=monto,
        deuda_actual=cooperante.deuda_restante
    )

    # 3. Lógica matemática: Restamos el abono a la deuda del cooperante
    cooperante.deuda_restante -= nueva_aportacion.monto_abonado

    # 4. Guardamos la transacción y la nueva deuda en la base de datos
    db.add(nueva_aportacion)
    db.add(cooperante)
    db.commit()
    db.refresh(nueva_aportacion)

    # Retornamos un resumen de la operación exitosa
    return {
        "mensaje": "Abono registrado con éxito",
        "tipo_recibo": nueva_aportacion.tipo_aportacion,
        "monto_cobrado": nueva_aportacion.monto_abonado,
        "nueva_deuda": cooperante.deuda_restante
    }