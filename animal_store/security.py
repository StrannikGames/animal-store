from datetime import UTC, datetime, timedelta

import jwt
from passlib.context import CryptContext


class PasswordHasher:
    def __init__(self):
        self.__context = CryptContext(schemes=["argon2"], deprecated="auto")

    def get_password_hash(self, password: str) -> str:
        return self.__context.hash(password)

    def compare_passwords(self, raw_password: str, password_hash: str) -> bool:
        return self.__context.verify(raw_password, password_hash)


class TokenManager:
    ALGORITHM = "HS256"

    def __init__(self, secret_key: str, lifetime: timedelta):
        self.__secret_key = secret_key
        self.__lifetime = lifetime

    def issue_token(self, user_id: int) -> str:
        return jwt.encode(
            {
                # по стандарту JWT "sub" должен быть строкой
                "sub": str(user_id),
                "exp": datetime.now(UTC) + self.__lifetime,
            },
            key=self.__secret_key,
            algorithm=self.ALGORITHM,
        )

    def verify_token(self, token: str) -> int | None:
        try:
            payload = jwt.decode(
                token, key=self.__secret_key, algorithms=[self.ALGORITHM]
            )
            return int(payload["sub"])
        except (jwt.InvalidTokenError, KeyError, ValueError):
            return None
