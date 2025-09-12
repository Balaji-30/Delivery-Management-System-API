from pydantic_settings import BaseSettings,SettingsConfigDict

class DatabaseSettings(BaseSettings):
    POSTGRES_USER: str
    POSTGRES_SERVER: str
    POSTGRES_SERVER_PORT: int
    POSTGRES_DB: str

    model_config = SettingsConfigDict(
        env_file="./.env", 
        env_ignore_empty=True,
        extra="ignore",
        env_file_encoding="utf-8") 
    
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}@{self.POSTGRES_SERVER}:{self.POSTGRES_SERVER_PORT}/{self.POSTGRES_DB}" 

database_settings = DatabaseSettings()
print(database_settings.POSTGRES_URL)