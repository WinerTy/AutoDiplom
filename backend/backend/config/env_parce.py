from pydantic_settings import BaseSettings
from pydantic import Field


class Configuration(BaseSettings):
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    TOKEN_LIFETIME_IN_DAYS: int = Field(env="TOKEN_LIFETIME_IN_DAYS", default=1)
    REFRESH_TOKEN_LIFETIME: int = Field(env="REFRESH_TOKEN_LIFETIME", default=7)
    API_VERSION: str = Field(env="API_VERSION", default="1.0.0")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Configuration()
