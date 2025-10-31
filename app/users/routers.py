from fastapi import HTTPException, Depends, Body, status, APIRouter
from app.database import SessionDep
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app import models
from app.users.schemas import UserLoginSchema, UserCreateSchema, UserResponse
from app.users.auth import (
    signJWT,
    decodeJWT,
    get_password_hash,
    verify_password
)
from sqlalchemy import select

users_router = APIRouter(
    prefix="/user",
    tags=["user"]
)

oauth2_scheme = HTTPBearer()


@users_router.post("/login", tags=["user"])
def user_login(session: SessionDep, user: UserLoginSchema = Body(...)):
    """
    Autentica o usuário, verifica a senha no banco e GERA o token JWT.
    """
    db_user = session.scalar(
        select(models.User).where(models.User.email == user.email)
    )

    if db_user and verify_password(user.password, db_user.password):
        return signJWT(db_user.id)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais de login inválidas!"
    )


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(oauth2_scheme)) -> dict:
    """Função de dependência para verificar o token JWT em rotas protegidas."""
    token = credentials.credentials

    payload = decodeJWT(token)

    if payload:
        return payload

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token inválido, ausente ou expirado."
    )


@users_router.post("/signup", response_model=UserResponse, tags=["user"])
def user_signup(user: UserCreateSchema, session: SessionDep):
    """
    Registra um novo usuário no banco de dados com a senha hasheada.
    """
    existing_user = session.scalar(
        select(models.User).where(models.User.email == user.email)
    )
    if existing_user:
        raise HTTPException(status_code=400, detail="O email já está registrado.")
    hashed_password = get_password_hash(user.password)

    db_user = models.User(email=user.email, password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user
