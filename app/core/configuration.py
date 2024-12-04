import os

APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL','postgresql://yoela:yoela@localhost:5432/dbgame')

APP_SECRET_KEY = os.getenv("APP_SECRET_KEY", "secret")
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "confidential")
TOKEN_MINUTES_LIFE_ADMIN=os.getenv("DBUSER", 60)

API_URL = os.getenv("API_URL", "f")

SERVER_HOST = os.environ.get("SERVER_HOST", '0.0.0.0') 
SERVER_PORT = int(os.environ.get("SERVER_PORT", "5000"))
DEBUG = os.environ.get("DEBUG", "false") == "true"

API_SECRET_KEY = os.getenv("API_SECRET_KEY", "DofluFngQjGpedWvVY1A8uyplHId-b6L")

WS_API_URL = os.getenv("WS_API_URL", "http://200.7.161.170:5000/api_v2")


