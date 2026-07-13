from pydantic import BaseModel
from typing import Optional

class UserCreate(BaseModel):
    name: str
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    name: str
    role: str

    class Config:
        orm_mode = True