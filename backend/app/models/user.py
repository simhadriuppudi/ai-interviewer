from sqlmodel import SQLModel, Field
from typing import Optional

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    full_name: Optional[str] = None
    is_active: bool = True

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

class UserCreate(UserBase):
    password: str

class UserRead(UserBase):
    id: int

class UserLogin(SQLModel):
    email: str
    password: str

class Token(SQLModel):
    access_token: str
    token_type: str
