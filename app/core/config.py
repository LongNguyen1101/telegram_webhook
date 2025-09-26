from pydantic import HttpUrl, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    telegram_token: str = Field(..., env="TELEGRAM_TOKEN")
    webhook_base_url: HttpUrl = Field(..., env="WEBHOOK_BASE_URL")
    server_dest_url: HttpUrl = Field(..., env="SERVER_DEST_URL")
    callback_secret: str = Field(..., env="CALLBACK_SECRET")
    request_timeout: int = Field(10, env="REQUEST_TIMEOUT")

    class Config:
        env_file = ".env"

settings = Settings()
