from pydantic import BaseModel, EmailStr
from typing import Optional

# Register schema
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str


# Login schema
class UserLogin(BaseModel):
    email: EmailStr
    password: str


# Response schema
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    bio: Optional[str]
    avatar: Optional[str]
    is_active: bool

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    name: Optional[str]=None
    bio: Optional[str]=None
    avatar: Optional[str]=None