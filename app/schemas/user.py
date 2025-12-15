from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Schema base con campos comunes
class UserBase(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    full_name: Optional[str] = None
    is_active: Optional[bool] = True


# Schema para crear usuario (incluye password)
class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)


# Schema para actualizar usuario (todos los campos opcionales)
class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    full_name: Optional[str] = None
    password: Optional[str] = Field(None, min_length=6, max_length=100)
    is_active: Optional[bool] = None


# Schema para respuestas (sin password)
class UserResponse(UserBase):
    id: int
    is_superuser: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # Permite convertir desde objetos SQLAlchemy


# Schema para login
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Schema para respuesta de login
class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse