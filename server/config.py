from pathlib import Path
from pydantic_settings import BaseSettings

_root = Path(__file__).resolve().parent.parent


class Cfg(BaseSettings):
    anthropic_api_key: str = ""
    model: str = "claude-sonnet-4-20250514"
    max_tokens: int = 4096

    model_config = {"env_file": str(_root / ".env"), "env_file_encoding": "utf-8"}


cfg = Cfg()
