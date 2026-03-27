from models.models import Aportacion
from datetime import datetime

class AportacionFactory:
    """
    Implementación del Patrón Factory.
    Se encarga de clasificar y fabricar el objeto Aportacion correcto
    (Abono Parcial o Liquidación Total) antes de enviarlo a la base de datos.
    """
    
    @staticmethod
    def procesar_pago(id_cooperante: int, monto_ingresado: float, deuda_actual: float) -> Aportacion:
        
        # 1. Validación básica
        if monto_ingresado <= 0:
            raise ValueError("El monto del abono debe ser mayor a 0.")
            
        # 2. La fábrica evalúa la situación y decide el tipo
        if monto_ingresado >= deuda_actual:
            tipo = "Liquidacion Total"
            # Si el cooperante da de más, solo le cobramos lo que debe
            monto_final = deuda_actual 
        else:
            tipo = "Abono Parcial"
            monto_final = monto_ingresado

        # 3. La fábrica "construye" el objeto y lo retorna listo para guardar
        return Aportacion(
            id_cooperante=id_cooperante,
            monto_abonado=monto_final,
            tipo_aportacion=tipo,
            fecha_pago=datetime.utcnow()
        )