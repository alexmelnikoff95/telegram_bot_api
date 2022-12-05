from pydantic import BaseSettings, AnyHttpUrl
from pydantic.tools import lru_cache


class Settings(BaseSettings):
    token: str
    vk: AnyHttpUrl
    youtube: AnyHttpUrl
    key: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def settings():
    return Settings()
