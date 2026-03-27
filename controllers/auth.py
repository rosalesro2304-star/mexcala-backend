from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from core.security import crear_token_acceso
from pydantic import BaseModel
from sqlmodel import Session, select
from fastapi import HTTPException, status
from models.models import Usuario
from database import get_session
from core.security import pwd_context

router = APIRouter(tags=["Autenticación"])

@router.post("/login")
# Agregamos "db: Session = Depends(get_session)" para poder consultar a los cobradores
def iniciar_sesion(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """
    Verifica las credenciales. 
    En un entorno de producción, aquí buscaríamos en la tabla Admin de PostgreSQL.
    """
    # Validación del administrador maestro
    if form_data.username == "admin" and form_data.password == "mexcala123":
        rol_asignado = "admin"
        
    else:
        # Si no es el admin maestro, buscamos al usuario en la base de datos de cobradores
        usuario_db = db.exec(select(Usuario).where(Usuario.username == form_data.username)).first()
        
        # Si no existe, o si la contraseña ingresada no coincide con la encriptada
        if not usuario_db or not pwd_context.verify(form_data.password, usuario_db.password_hash):
            # Si se equivoca, devolvemos un error 401 (No Autorizado)
            raise HTTPException(
                status_code=401, 
                detail="Usuario o contraseña incorrectos"
            )
        # Si pasó la verificación, le asignamos su rol
        rol_asignado = usuario_db.rol

    # Si es correcto (ya sea admin o cobrador), fabricamos su Token JWT
    token = crear_token_acceso({"sub": form_data.username})
    
    # FastAPI exige que la respuesta tenga este formato exacto
    # NUEVO: Mandamos el rol hacia el frontend para que sepa qué botones ocultar
    return {
        "access_token": token, 
        "token_type": "bearer",
        "rol": rol_asignado
    }
    
# 1. Molde para recibir los datos desde el frontend
class UsuarioRegistro(BaseModel):
    username: str
    password: str

# 2. La ruta que procesa el registro
@router.post("/registro", status_code=status.HTTP_201_CREATED)
def registrar_usuario(nuevo_usuario: UsuarioRegistro, db: Session = Depends(get_session)):
    
    # Verificamos que el nombre de usuario no exista ya
    usuario_existente = db.exec(select(Usuario).where(Usuario.username == nuevo_usuario.username)).first()
    if usuario_existente:
        raise HTTPException(status_code=400, detail="Este nombre de usuario ya está en uso")
    
    # Encriptamos la contraseña para que sea segura
    contrasena_encriptada = pwd_context.hash(nuevo_usuario.password)
    
    # Creamos el registro para guardarlo en PostgreSQL
    usuario_db = Usuario(
        username=nuevo_usuario.username,
        password_hash=contrasena_encriptada,
        rol="cobrador"
    )
    
    db.add(usuario_db)
    db.commit()
    
    return {"mensaje": f"Cobrador '{usuario_db.username}' registrado exitosamente"}