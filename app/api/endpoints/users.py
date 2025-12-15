from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.schemas.user import UserCreate, UserUpdate, UserResponse, UserLogin, TokenResponse
from app.services.user_service import UserService

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registrar un nuevo usuario.
    
    - **email**: Email único del usuario
    - **username**: Nombre de usuario único
    - **password**: Contraseña (se guardará hasheada)
    - **full_name**: Nombre completo (opcional)
    """
    # Verificar si el email ya existe
    existing_user = await UserService.get_user_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )
    
    # Verificar si el username ya existe
    existing_username = await UserService.get_user_by_username(db, user.username)
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El nombre de usuario ya está en uso"
        )
    
    # Crear usuario
    new_user = await UserService.create_user(db, user)
    return new_user


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """
    Iniciar sesión (autenticar usuario).
    
    - **email**: Email del usuario
    - **password**: Contraseña
    """
    user = await UserService.authenticate_user(db, credentials.email, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    
    # En un sistema real, aquí generarías un JWT token
    # Para este ejemplo, devolvemos un token simple
    return TokenResponse(
        access_token=f"token_for_user_{user.id}",
        user=user
    )


@router.get("/users", response_model=List[UserResponse])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener lista de usuarios con paginación.
    
    - **skip**: Número de registros a saltar (default: 0)
    - **limit**: Número máximo de registros (default: 100)
    """
    users = await UserService.get_all_users(db, skip=skip, limit=limit)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Obtener un usuario específico por ID.
    """
    user = await UserService.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return user


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    """
    Actualizar un usuario existente.
    
    Todos los campos son opcionales.
    """
    updated_user = await UserService.update_user(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return updated_user


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    """
    Eliminar un usuario.
    """
    deleted = await UserService.delete_user(db, user_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuario no encontrado"
        )
    return None