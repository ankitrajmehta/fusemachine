from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    PROJ_ROOT: Path = Path(__file__).resolve().parents[1]
    MODELS_DIR: Path = PROJ_ROOT / "models"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
