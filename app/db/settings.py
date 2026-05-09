import os
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

class Settings(BaseSettings):
    PORT: int
    HOST: str
    DATABASE: str
    USER: str
    PASSWORD: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15

    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, '.env'),
        env_file_encoding="utf-8",
    )


config = Settings()
print("DB CONFIG:")
print("USER:", config.USER)
print("PASSWORD:", config.PASSWORD)
print("HOST:", config.HOST)
print("PORT:", config.PORT)
print("DATABASE:", config.DATABASE)
