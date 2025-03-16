from pydantic_settings import BaseSettings, SettingsConfigDict

_ENV_PATH =  '.env.local'
_ENV_PREFIX = 'warehouse_management_'


class Settings(BaseSettings):
    DATABASE_URL = 'sqlite:///warehouse.db'

    model_config = SettingsConfigDict(env_prefix=_ENV_PREFIX, env_file=_ENV_PATH, extra='ignore')

settings = Settings()
