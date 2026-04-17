from dataclasses import dataclass
from pathlib import Path
from typing import Optional
import os


@dataclass
class AppConfig:
    """Configuración de la aplicación."""
    
    database_url: str = "sqlite:///data/taller.db"
    debug: bool = False
    log_level: str = "INFO"
    
    @classmethod
    def from_env(cls) -> "AppConfig":
        """Carga configuración desde variables de entorno."""
        return cls(
            database_url=os.environ.get("DATABASE_URL", "sqlite:///data/taller.db"),
            debug=os.environ.get("DEBUG", "false").lower() == "true",
            log_level=os.environ.get("LOG_LEVEL", "INFO")
        )
    
    @classmethod
    def from_file(cls, path: Path) -> "AppConfig":
        """Carga configuración desde archivo JSON (futuro)."""
        return cls.from_env()


class Settings:
    """Administrador de configuración global."""
    
    _instance: Optional[AppConfig] = None
    
    @classmethod
    def get(cls) -> AppConfig:
        if cls._instance is None:
            cls._instance = AppConfig.from_env()
        return cls._instance
    
    @classmethod
    def reset(cls):
        cls._instance = None