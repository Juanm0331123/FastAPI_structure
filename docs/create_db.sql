-- Script SQL para crear la base de datos y tabla de usuarios
-- NOTA: FastAPI creará automáticamente las tablas al iniciar
-- Este script es solo de referencia/backup

-- Crear base de datos (ejecutar como superusuario)
CREATE DATABASE fastapi_db
    WITH 
    OWNER = postgres
    ENCODING = 'UTF8'
    CONNECTION LIMIT = -1;

-- Conectarse a la base de datos fastapi_db antes de continuar
\c fastapi_db

-- Crear tabla users (FastAPI lo hace automáticamente, esto es solo referencia)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    email VARCHAR NOT NULL UNIQUE,
    username VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    full_name VARCHAR,
    is_active BOOLEAN DEFAULT TRUE,
    is_superuser BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Crear índices para mejor rendimiento
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);

-- Ver la estructura de la tabla
\d users

-- Comentarios en las columnas
COMMENT ON TABLE users IS 'Tabla de usuarios del sistema';
COMMENT ON COLUMN users.email IS 'Email único del usuario';
COMMENT ON COLUMN users.username IS 'Nombre de usuario único';
COMMENT ON COLUMN users.hashed_password IS 'Contraseña hasheada con bcrypt';
COMMENT ON COLUMN users.is_active IS 'Indica si el usuario está activo';
COMMENT ON COLUMN users.is_superuser IS 'Indica si el usuario es administrador';
