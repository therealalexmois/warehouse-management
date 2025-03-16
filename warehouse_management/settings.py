"""Настройка параметров приложения с помощью Pydantic.

Модуль определяет класс `Settings`, который загружает конфигурацию из переменных окружения
и файла `.env.local` для локальной разработки.ariables and an optional `.env.local` file for local development.
"""

import os
from enum import Enum

from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_ENV = 'local'

_ENV_PREFIX: str = 'WAREHOUSE_MANAGEMENT_'
_ENV_FILE: str | None = '.env.local' if os.environ.get(f'{_ENV_PREFIX}ENV', DEFAULT_ENV) == DEFAULT_ENV else None


class Env(str, Enum):
    """Перечисление допустимых значений среды."""

    LOCAL = 'local'
    DEVELOPMENT = 'development'
    PRODUCTION = 'production'


class DatabaseSettings(BaseSettings):
    """Настройки конфигурации базы данных."""

    url: str = 'sqlite:///warehouse.db'

    model_config = SettingsConfigDict(
        env_prefix=_ENV_PREFIX,
        env_file=_ENV_FILE,
        extra='ignore',
    )


class Settings(BaseSettings):
    """Основные настройки приложения, содержащие все конфигурации."""

    env: Env = Env.LOCAL
    database: DatabaseSettings = DatabaseSettings()

    model_config = SettingsConfigDict(
        env_prefix=_ENV_PREFIX,
        env_file=_ENV_FILE,
        extra='ignore',
    )
