import yaml
from pathlib import Path
from src.config.config_model import Config
from src.config.config_validator import validate

def load_config(config_path: Path) -> Config:
    if not config_path.exists():
        raise FileNotFoundError(f"Configuration file not found: {config_path}")

    with open(config_path, "r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML structure in {config_path}")

    validate(data)

    return Config(
        schema=data.get("schema"),
        primary_keys=data.get("primary_keys"),
        foreign_keys=data.get("foreign_keys"),
    )
