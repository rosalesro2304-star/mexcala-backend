from sqlmodel import SQLModel, create_engine, Session

# Nota: Cambiaremos estos datos por los de tu PostgreSQL local más adelante
DATABASE_URL = "postgresql://neondb_owner:npg_l4RAvIVePUN0@ep-rapid-meadow-anmoizzr.c-6.us-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require"

engine = create_engine(DATABASE_URL, echo=True)


class DatabaseManager:
    """Implementación del Patrón Singleton para la Base de Datos"""
    _instance = None

    def __new__(cls):
        # Si la instancia no existe, la crea. Si ya existe, devuelve la misma.
        if cls._instance is None:
            print("Inicializando conexión única a PostgreSQL (Singleton)...")
            cls._instance = super(DatabaseManager, cls).__new__(cls)
            # echo=True nos permite ver en la consola el SQL que se está ejecutando (útil al programar)
            cls._instance.engine = create_engine(DATABASE_URL, echo=True)
        return cls._instance

    def get_session(self):
        """Genera una sesión para interactuar con la base de datos"""
        return Session(self.engine)

# Instancia global que exportaremos al resto de la aplicación
db_manager = DatabaseManager()

# Función inyectora para las rutas de FastAPI
def get_db():
    with db_manager.get_session() as session:
        yield session

def create_db_and_tables():
    """Función para generar las tablas físicamente en PostgreSQL"""
    SQLModel.metadata.create_all(db_manager.engine)

def get_session():
    with Session(engine) as session:
        yield session