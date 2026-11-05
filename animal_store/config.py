import os
from datetime import timedelta

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://admin:qwerty12@db:5432/animal_store",
)

# Сгенерировать свой ключ: openssl rand -base64 48
SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")

TOKEN_LIFETIME = timedelta(minutes=int(os.getenv("TOKEN_LIFETIME_MINUTES", "60")))

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))
