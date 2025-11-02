import yaml
from pathlib import Path

from src.config.config_model import Config

class ConfigLoader:
    @staticmethod
    def load(config_path: Path) -> Config:
        if not config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {config_path}")
       
        with open(config_path, "r", encoding="utf-8") as file:
            if config_path.suffix.lower() in [".yaml", ".yml"]:
                data = yaml.safe_load(file)
            else:
                raise ValueError(f"Unsupported config file type: {config_path.suffix}")

        return Config(**data)