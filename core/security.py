from datetime import datetime, timedelta
from jose import jwt
from passlib.context import CryptContext

# Configuraciones de seguridad
SECRET_KEY = "mexcala_super_secreto_2026" # Esta es la firma digital de tu API
ALGORITHM = "HS256"
TIEMPO_EXPIRACION_MINUTOS = 30 # El administrador se cerrará solo en 30 minutos

# Herramienta para encriptar contraseñas (aunque usemos una fija por ahora, es buena práctica)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def crear_token_acceso(data: dict):
    """Genera un Token JWT válido para el administrador"""
    a_encriptar = data.copy()
    expiracion = datetime.utcnow() + timedelta(minutes=TIEMPO_EXPIRACION_MINUTOS)
    a_encriptar.update({"exp": expiracion})
    
    # Fabricamos el token usando la llave secreta
    token_jwt = jwt.encode(a_encriptar, SECRET_KEY, algorithm=ALGORITHM)
    return token_jwt