from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from schemas.user import UserCreate, UserResponse, UserLogin
from core.security import hash_password, verify_password, create_access, get_current_user

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

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == credentials.email).first()
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    if not verify_password(credentials.password, user.password_hash):
         raise HTTPException(status_code=401, detail="Invalid credentials")
        
    access_token = create_access(data={"user_id": user.id})    
    return {"access_token": access_token, "token_type": "bearer"}
