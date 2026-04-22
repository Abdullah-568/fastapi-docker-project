from asyncio import create_task

from fastapi.security import OAuth2PasswordRequestForm

import models
import schemas
from database import engine,get_db
from fastapi import FastAPI,HTTPException,Depends
from sqlalchemy.orm import Session
from typing import List
from auth import verify_password
from auth import create_token
from auth import hash_password
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)


app=FastAPI()
app.add_middleware(          # ← add this block
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/students",response_model=List[schemas.StudentResponse])
def get_students(db:Session=Depends(get_db)):
    studemts=db.query(models.Student).all()
    return studemts

@app.get("/students/{student_id}")
def get_student(student_id:int,db: Session=Depends(get_db)):
    student=db.query(models.Student).filter(models.Student.id==student_id).first()
    if not student:
        raise HTTPException(status_code=404,detail="not found")
    return student

@app.post("/students")
def create_student(student:schemas.StudentCreate, db: Session =Depends(get_db)):
    db_student=models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student

@app.post("/register",response_model=schemas.UserResponse)
def register(user:schemas.userCreate,db: Session=Depends(get_db)):
    existing_user=db.query(models.User).filter(models.User.username == user.username).first()
    if existing_user:
        raise HTTPException(
            status_code=404,
            detail="username exiss"
        )
    
    existing_email=db.query(models.User).filter(
        models.User.email == user.email
    ).first()
    if existing_email:
        raise HTTPException(
            status_code=400,
            detail="email exists"
        )
    hashed=hash_password(user.password)

    db_user=models.User(
        username=user.username,
        email=user.email,
        password=hashed

    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.post("/login",response_model=schemas.Token)
def login(form_data:OAuth2PasswordRequestForm = Depends(),  db:Session = Depends(get_db)):
    user = db.query (models.User).filter(models.User.username == form_data.username). first()
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=404,
            detail="wrong entry "

        )
    token=create_token(user.username)
    return{
        "access_token":token,
        "token_type":"bearer"
    }

###NOW THE CONCEPT OF MIDDLEWARE CORS##
###  MIDDLEWARE CORS IS APPLIED TO ACCEPT TRAFFIC FROM OTHER PORTS , IT ISNUSEFUL WHEN FRONENDS WANTS TO NERACT AN DIN PRODUCTIONS ##

## we have added middleswhere under app=fastapi()####