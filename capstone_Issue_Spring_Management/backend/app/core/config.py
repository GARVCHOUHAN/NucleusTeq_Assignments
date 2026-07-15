import os
from dotenv import load_dotenv

load_dotenv()
def _get_env(name: str, default: str = "") -> str:
    return os.getenv(name, default).strip()

class Settings:
    MONGO_URI = _get_env("MONGO_URI")
    DATABASE_NAME = _get_env("DATABASE_NAME", "issue_sprint_management")
    SECRET_KEY = _get_env("SECRET_KEY", "change-this-secret")
    ALGORITHM = _get_env("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = int(_get_env("ACCESS_TOKEN_EXPIRE_MINUTES", "180"))

settings = Settings()
