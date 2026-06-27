from typing import Optional

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str


class UserResponse(BaseModel):
    name: str
    id: int
    

    class Config:
        orm_mode = True


class UserUpdate(BaseModel):
    name: Optional[str] = None


class StudentCreate(BaseModel):
    name: str


class CourseCreate(BaseModel):
    name: str

class CommentCreate(BaseModel):
    user_id: int
    text: str

class ProfileCreate(BaseModel):
    user_id: int
    name: str
    