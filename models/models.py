from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime

# 1. Tabla de Administradores (Para el inicio de sesión)
class Admin(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    usuario: str = Field(unique=True, index=True)
    password_hash: str
    rol: str = Field(default="comite")

# 2. Tabla de Cooperantes (Los ciudadanos de Mexcala)
class Cooperante(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre_completo: str = Field(index=True)
    # Por regla de negocio, todos inician con la deuda de la cuota anual
    deuda_restante: float = Field(default=2000.0) 
    
    # Relación: Un cooperante puede tener muchas aportaciones
    aportaciones: List["Aportacion"] = Relationship(back_populates="cooperante")

# 3. Tabla de Aportaciones (El historial de pagos)
class Aportacion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    monto_abonado: float
    fecha_pago: datetime = Field(default_factory=datetime.utcnow)
    # Aquí es donde entrará a trabajar nuestro patrón Factory más adelante
    tipo_aportacion: str 
    
    # Llave foránea que conecta con el Cooperante
    id_cooperante: int = Field(foreign_key="cooperante.id")
    cooperante: Optional[Cooperante] = Relationship(back_populates="aportaciones")

    # NUEVA TABLA PARA LOS USUARIOS (ADMIN Y COBRADORES)
class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(unique=True, index=True) 
    password_hash: str # Aquí se guardará la contraseña encriptada
    rol: str = Field(default="cobrador") # Por defecto, todos serán cobradores