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

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = _base_config
    
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}@{self.POSTGRES_SERVER}:{self.POSTGRES_SERVER_PORT}/{self.POSTGRES_DB}"

    def REDIS_URL(self, db:int):
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{db}" 

class SecuritySettings(BaseSettings):
    JWT_SECRET : str
    JWT_ALGORITHM: str

    model_config = _base_config

class NotificationsSettings(BaseSettings):
    MAIL_USERNAME: str
    MAIL_PASSWORD: str
    MAIL_PORT: int
    MAIL_SERVER: str
    MAIL_FROM: str
    MAIL_FROM_NAME: str
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    USE_CREDENTIALS: bool = True
    VALIDATE_CERTS: bool = True

    RESEND_API_KEY: str

    TWILIO_SID: str
    TWILIO_AUTH_TOKEN: str
    TWILIO_NUMBER: str

    model_config = _base_config

class AppSettings(BaseSettings):
    APP_NAME: str = "Shippin"
    APP_VERSION: str = "1.0.0"
    APP_DOMAIN: str = "localhost:5173"
    BACKEND_APP_DOMAIN: str="localhost:8000"

database_settings = DatabaseSettings()
security_settings = SecuritySettings()
notifications_settings = NotificationsSettings()
app_settings = AppSettings()