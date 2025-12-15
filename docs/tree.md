FastAPI_test/
├── .env                         # Variables de entorno (NO subir a git)
├── .env.example                 # Plantilla de variables de entorno
├── .gitignore                   # Archivos a ignorar en git
├── README.md                    # Documentación del proyecto
├── requirements.txt             # Dependencias de Python
├── venv/                        # Entorno virtual
├── docs/
│   ├── create_db.sql           # Script SQL para crear la BD
│   └── tree.md                 # Este archivo (estructura del proyecto)
└── app/
    ├── __init__.py
    ├── main.py                 # Punto de entrada de la aplicación
    ├── api/                    # Capa de presentación (Endpoints REST)
    │   ├── __init__.py
    │   ├── router.py           # Router principal que agrupa todas las rutas
    │   └── endpoints/
    │       ├── __init__.py
    │       └── users.py        # Endpoints CRUD de usuarios + login
    ├── core/                   # Configuraciones
    │   ├── __init__.py
    │   └── config.py           # Settings y variables de entorno
    ├── db/                     # Capa de datos
    │   ├── __init__.py
    │   ├── base.py             # Base declarativa de SQLAlchemy
    │   └── session.py          # Conexión a PostgreSQL (async)
    ├── models/                 # Modelos ORM (Tablas de la BD)
    │   ├── __init__.py
    │   └── user.py             # Modelo User (tabla users)
    ├── schemas/                # Pydantic (Validación y Serialización)
    │   ├── __init__.py
    │   └── user.py             # Schemas para User (request/response)
    └── services/               # Lógica de Negocio
        ├── __init__.py
        └── user_service.py     # Servicio con CRUD y hash de contraseñas


## 📝 Convenciones de Nombres (REST API)

### Archivos y Módulos
- **Modelos**: `user.py` (singular) - Representa una entidad de la BD
- **Schemas**: `user.py` (singular) - Valida datos de entrada/salida
- **Services**: `user_service.py` - Lógica de negocio
- **Endpoints**: `users.py` (plural) - Rutas REST para el recurso

### Endpoints REST
- `POST /users` o `/register` - Crear recurso
- `GET /users` - Listar recursos
- `GET /users/{id}` - Obtener recurso específico
- `PUT /users/{id}` - Actualizar recurso completo
- `PATCH /users/{id}` - Actualizar recurso parcial
- `DELETE /users/{id}` - Eliminar recurso

### Códigos de Estado HTTP
- `200 OK` - Éxito en GET, PUT, PATCH
- `201 Created` - Recurso creado exitosamente
- `204 No Content` - Eliminación exitosa
- `400 Bad Request` - Datos inválidos
- `401 Unauthorized` - No autenticado
- `403 Forbidden` - No autorizado
- `404 Not Found` - Recurso no encontrado
- `500 Internal Server Error` - Error del servidor