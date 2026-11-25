from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5435/auth_db"

    JWT_SECRET_KEY: str = "super-secret-key-change-me"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 60
    KAFKA_BROKERS: str = "kafka:9092"

    class Config:
        env_file = ".env"


settings = Settings()