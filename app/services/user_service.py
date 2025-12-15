from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import bcrypt
from typing import Optional, List

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Servicio con la lógica de negocio para usuarios"""

    @staticmethod
    def hash_password(password: str) -> str:
        """Genera hash de la contraseña usando bcrypt"""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verifica si la contraseña coincide con el hash"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    @staticmethod
    async def get_user_by_id(db: AsyncSession, user_id: int) -> Optional[User]:
        """Obtiene un usuario por ID"""
        result = await db.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_email(db: AsyncSession, email: str) -> Optional[User]:
        """Obtiene un usuario por email"""
        result = await db.execute(select(User).where(User.email == email))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_user_by_username(db: AsyncSession, username: str) -> Optional[User]:
        """Obtiene un usuario por username"""
        result = await db.execute(select(User).where(User.username == username))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_all_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
        """Obtiene todos los usuarios con paginación"""
        result = await db.execute(select(User).offset(skip).limit(limit))
        return result.scalars().all()

    @staticmethod
    async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
        """Crea un nuevo usuario"""
        # Hash de la contraseña
        hashed_password = UserService.hash_password(user_create.password)
        
        # Crear instancia del modelo
        db_user = User(
            email=user_create.email,
            username=user_create.username,
            full_name=user_create.full_name,
            hashed_password=hashed_password,
            is_active=user_create.is_active,
        )
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def update_user(db: AsyncSession, user_id: int, user_update: UserUpdate) -> Optional[User]:
        """Actualiza un usuario existente"""
        # Buscar usuario
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return None

        # Actualizar solo los campos proporcionados
        update_data = user_update.model_dump(exclude_unset=True)
        
        # Si se proporciona nueva contraseña, hashearla
        if "password" in update_data:
            update_data["hashed_password"] = UserService.hash_password(update_data.pop("password"))
        
        for field, value in update_data.items():
            setattr(db_user, field, value)
        
        await db.commit()
        await db.refresh(db_user)
        return db_user

    @staticmethod
    async def delete_user(db: AsyncSession, user_id: int) -> bool:
        """Elimina un usuario"""
        db_user = await UserService.get_user_by_id(db, user_id)
        if not db_user:
            return False
        
        await db.delete(db_user)
        await db.commit()
        return True

    @staticmethod
    async def authenticate_user(db: AsyncSession, email: str, password: str) -> Optional[User]:
        """Autentica un usuario (verifica credenciales)"""
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not UserService.verify_password(password, user.hashed_password):
            return None
        return user