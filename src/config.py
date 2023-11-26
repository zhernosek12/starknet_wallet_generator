import yaml

from pathlib import Path
from pydantic import BaseModel


class AppConfig(BaseModel):
    wallets_count: int


_config_path = Path(__file__).resolve().parent.parent / "config.yaml"
with _config_path.open(encoding="utf-8") as f:
    _data = yaml.safe_load(f)

config = AppConfig.model_validate(_data)
