from pydantic import BaseModel, EmailStr
from typing import Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    pass


class UserOut(BaseModel):
    id: int
    email: str
    name: str
    role: str
    organization: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserRegister(BaseModel):
    email: EmailStr
    name: str
    password: str
    organization: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut
