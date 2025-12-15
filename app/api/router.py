from fastapi import APIRouter
from app.api.endpoints import users

api_router = APIRouter()

# Incluir todas las rutas de endpoints
api_router.include_router(
    users.router,
    tags=["users"]
)