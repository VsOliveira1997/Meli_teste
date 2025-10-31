# app/auth.py

import time
from typing import Dict
from passlib.context import CryptContext
import jwt

password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
JWT_SECRET = "LG/gT4yCbwswCQb3Z7prg5L+hP4eKmZScWKjHf8ALfaSuNTsNM8yAbR5O3f2P8oF"
JWT_ALGORITHM = "HS256"


def get_password_hash(password: str) -> str:
    """Cria o hash da senha."""
    return password_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha em texto plano corresponde ao hash."""
    return password_context.verify(plain_password, hashed_password)


def token_response(token: str) -> Dict[str, str]:
    """Estrutura a resposta do token."""
    return {"access_token": token, "token_type": "bearer"}


def signJWT(user_id: int) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "expires": time.time() + 3600  # Expira em 1 hora
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return token_response(token)


def decodeJWT(token: str) -> dict:
    try:
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        if decoded_token.get("expires", 0) >= time.time():
            return decoded_token

        return {}
    except:
        return {}