airflow-monitor-api/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Punto de entrada de la app
│   ├── api/                     # Capa de presentación (Rutas)
│   │   ├── __init__.py
│   │   ├── api_v1/
│   │   │   ├── __init__.py
│   │   │   ├── router.py        # Agrupador de rutas
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       └── status.py    # TU CONTROLLER: aquí va la lógica del endpoint
│   ├── core/                    # Configuraciones
│   │   ├── __init__.py
│   │   └── config.py            # Variables de entorno y settings
│   ├── db/                      # Capa de datos
│   │   ├── __init__.py
│   │   ├── session.py           # Conexión a la BD (SQLAlchemy)
│   │   └── base.py              # Importador de modelos
│   ├── models/                  # Modelos SQL (Tablas de Airflow)
│   │   ├── __init__.py
│   │   └── dag_run.py           # Mapeo de la tabla 'dag_run' de Airflow
│   ├── schemas/                 # Pydantic (Validación y Serialización)
│   │   ├── __init__.py
│   │   └── monitor.py           # Cómo se ve el JSON de respuesta
│   └── services/                # Lógica de Negocio
│       ├── __init__.py
│       └── status_service.py    # Lógica para interpretar si falló o no
├── .env                         # Credenciales (NO subir a git)
├── requirements.txt
└── Dockerfile