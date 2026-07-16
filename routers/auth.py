from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from schemas.user import UserCreate, UserResponse
from core.security import hash_password

router = APIRouter()

@router.post("/signup", response_model= UserResponse)
def signup(user_data: UserCreate, db: Session = Depends(get_db)):
    hashed_password= hash_password(user_data.password)

    new_user = User(
        name = user_data.name,
        email = user_data.email,
        password_hash = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return  new_user

