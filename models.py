from sqlalchemy import Column,Integer,String,Boolean
from database import Base

class Student(Base):
    __tablename__="Students"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String,nullable=False)
    age=Column(Integer,nullable=False)
    grade=Column(String,nullable=False)
    passed=Column(Boolean,default=True)


class User(Base):
    __tablename__= "users"

    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True, nullable=False)
    email=Column(String,unique=True,nullable=False)
    password=Column(String,nullable=False)