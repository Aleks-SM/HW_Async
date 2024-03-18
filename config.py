import os
from dotenv import load_dotenv


direnv = os.path.join(os.path.abspath(os.path.dirname(__file__)), ".env")
load_dotenv(direnv)

POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "secret")
POSTGRES_USER = os.getenv("POSTGRES_USER", "user")
POSTGRES_DB = os.getenv("POSTGRES_DB", "adv_db")
POSTGRES_HOST = os.getenv("POSTGRES_HOST", "127.0.0.1")
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5431")
TYPE_DB = os.getenv("TYPE_DB", "postgresql")