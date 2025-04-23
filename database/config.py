from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    SECRET_KEY: str
    FLASK_ENV: str
    DEBUG: bool

    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    class Config:
        env_file = (Path(__file__).parent.parent.resolve() / '.env')
        extra = 'allow'


settings = Settings()
