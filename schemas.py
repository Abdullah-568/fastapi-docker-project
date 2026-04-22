from pydantic import BaseModel
from typing import Optional

# used when CREATING student
# no id — database creates it automatically
class StudentCreate(BaseModel):
    name: str
    age: int
    grade: str
    passed: bool = True

# used when RETURNING student
# includes id — because it exists in database
class StudentResponse(BaseModel):
    id: int
    name: str
    age: int
    grade: str
    passed: bool

    class Config:
        from_attributes = True

class userCreate(BaseModel):
    username:str
    email:str
    password:str

class UserResponse(BaseModel):
    id:int
    username:str
    email:str

    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token: str
    token_type:str