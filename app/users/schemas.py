from pydantic import BaseModel, EmailStr

class UserLoginSchema(BaseModel):
    email: EmailStr
    password: str


class UserCreateSchema(BaseModel):
    """
    Define os dados de entrada necessários para registrar um novo usuário.
    """
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True