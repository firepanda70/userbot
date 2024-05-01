from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


class Confg(BaseSettings):
    model_config = SettingsConfigDict(extra='ignore')
    db_url: str
    api_id: int
    api_hash: str
    
def get_config(env_file: Path | None = None):
    if not env_file:
        return Confg()
    return Confg(_env_file = env_file)
