from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class UserRole(str, Enum):
    USER = "USER"
    COMPANY = "COMPANY"

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    role: Optional[UserRole] = UserRole.USER
    password: str
