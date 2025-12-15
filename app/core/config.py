from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str
    PROJECT_NAME: str = "FastAPI Project"

    # Construimos la URL automáticamente usando una propiedad
    @property
    def DATABASE_URL(self) -> str:
        # Estructura: postgresql+psycopg://user:password@host:port/dbname
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = ".env"
        extra = "ignore" 

settings = Settings()