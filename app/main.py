# app/main.py

from fastapi import FastAPI, HTTPException, status, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from .database import SessionLocal, engine
from .schemas import UserCreate, UserRead
from .models import Base, UserDB

app = FastAPI()
# Uncomment this line to reset DB
# Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Get all users
@app.get("/api/users", response_model=list[UserRead])
def list_users(db: Session = Depends(get_db)):
    # stmt is a python representation of a SQL query
    stmt = select(UserDB).order_by(UserDB.id)
    # scalars pulls the UserDB object out of the rows
    return list(db.execute(stmt).scalars())

#Get user by id
@app.get("/api/users/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

#Create user 
@app.post("/api/users", status_code=status.HTTP_201_CREATED)
def add_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = UserDB(**payload.model_dump())
    db.add(user)
    try:
        db.commit()
        db.refresh(user)
    # Unique fields in models.py are the ones used to verify if a student exists 
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    return user

# Update User
@app.put("/api/users/update/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserCreate, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    for key, value in payload.model_dump().items():
        setattr(user, key, value)
    try: 
        db.commit()
        db.refresh(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email or Student ID already exists")
    return user
    

#Delete User
@app.delete("/api/users/delete/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(UserDB, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    db.delete(user)
    db.commit()


     