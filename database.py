from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# connection string
# format: postgresql://username:password@host:port/database_name
DATABASE_URL =os.getenv( 
              "DATABASE_URL",
              "postgresql://postgres:postgress123@localhost:5432/fastapi_db"
               )
# create engine — connection to database
engine = create_engine(DATABASE_URL)

# each request gets its own session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# base class for all models
Base = declarative_base()

# dependency — gives database session to endpoints
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()