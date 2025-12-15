from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.router import api_router
from app.db.session import engine
from app.db.base import Base

# IMPORTANTE: Importar los modelos aquí para que Base.metadata los reconozca
# Si tienes más modelos, agrégalos aquí.
from app.models.user import User

@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- INICIO ---
    print(f"🚀 Conectando a {settings.DB_HOST} y creando tablas...")
    async with engine.begin() as conn:
        # Crea las tablas automáticamente si no existen
        await conn.run_sync(Base.metadata.create_all)
    
    yield # Aquí corre la aplicación
    
    # --- APAGADO ---
    print("🛑 Cerrando conexión a base de datos...")
    await engine.dispose()

app = FastAPI(
    title=settings.PROJECT_NAME,
    lifespan=lifespan
)

# Incluir rutas
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def root():
    return {
        "message": "API Activa", 
        "connected_to": settings.DB_NAME,
        "docs": "/docs"
    }