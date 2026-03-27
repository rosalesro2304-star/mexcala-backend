from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
# Importamos los modelos para que el motor los detecte al arrancar
from models.models import Admin, Cooperante, Aportacion 
# Importamos nuestros nuevos controladores
from controllers import cooperantes, aportaciones
from controllers import cooperantes, aportaciones, auth


app = FastAPI(
    title="API - Sistema de Cooperaciones Mexcala",
    description="Backend con FastAPI, SQLModel y Patrones de Diseño",
    version="1.0.0"
)

# --- CONFIGURACIÓN DE CORS (NUEVO) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # En producción se pone la IP de tu frontend, por ahora permitimos todo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# -------------------------------------

# Este evento se ejecuta justo antes de que el servidor empiece a recibir peticiones
@app.on_event("startup")
def on_startup():
    print("Iniciando servidor y verificando la base de datos...")
    create_db_and_tables()

app.include_router(cooperantes.router)
app.include_router(aportaciones.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"mensaje": "¡El API de Mexcala está funcionando correctamente!"}