from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    MAX_LOG_FILE_SIZE: int = 10 * 1024 * 1024  # 10 MB
    BACKUP_COUNT: int = 5
    ALLOWED_HOSTS: list[str] = ["localhost", "127.0.0.1"]

    class Config:
        # make sure add .env file
        # env_file = ".env"
        model_config = SettingsConfigDict(case_sensitive=True)


config = Settings()
