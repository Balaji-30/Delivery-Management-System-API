from pydantic_settings import BaseSettings,SettingsConfigDict

_base_config=SettingsConfigDict(
        env_file="./.env", 
        env_ignore_empty=True,
        extra="ignore")

class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_SERVER: str
    POSTGRES_SERVER_PORT: int
    POSTGRES_DB: str

    model_config = _base_config
    
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}@{self.POSTGRES_SERVER}:{self.POSTGRES_SERVER_PORT}/{self.POSTGRES_DB}" 

class SecuritySettings(BaseSettings):
    JWT_SECRET : str
    JWT_ALGORITHM: str

    model_config = _base_config

database_settings = DatabaseSettings()
security_settings = SecuritySettings()