from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    redis_url: str = "redis://localhost:6379/0"
    rabbitmq_url: str = "amqp://guest:guest@localhost:5672/"
    gmail_address: str
    gmail_app_password: str
    virtual_sensor_id: str | None = None
    sentry_dsn: str | None = None
    environment: str = "development"
    virtual_sensor_interval_seconds: int = 60

    class Config:
        env_file = ".env"

settings = Settings()