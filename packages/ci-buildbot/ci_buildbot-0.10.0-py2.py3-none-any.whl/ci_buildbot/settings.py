from pathlib import Path
from typing import Optional

from jinja2 import FileSystemLoader, Environment
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


templates_path = Path(__file__).parent / 'templates'
jinja_env = Environment(
    loader=FileSystemLoader(str(templates_path))
)


class Settings(BaseSettings):
    """
    See https://docs.pydantic.dev/latest/usage/pydantic_settings/ for details on
    using and overriding this.
    """
    api_token: Optional[str] = Field(None, validation_alias='slack_api_token')

    debug: bool = False

    channel: str = "jenkins"

    statsd_host: str = 'scope.cloud.caltech.edu'
    statsd_port: int = 8125
    statsd_prefix: str = 'ci-buildbot.test'

    model_config = SettingsConfigDict(
        case_sensitive=False,
        env_file='.env',
        env_file_encoding='utf-8',
    )
