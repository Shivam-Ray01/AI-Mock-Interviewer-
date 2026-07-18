from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from database import get_db
from models.users import User
from dotenv import load_dotenv
import bcrypt
import os
import jwt

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRY = int(os.getenv("ACCESS_TOKEN_EXPIRY"))

def hash_password(password : str):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt(rounds=12)
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    is_match = bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))
    return is_match

def create_access(data:dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRY) # helps in Sessionin expiration
    to_encode.update({"exp": expire})   # in this update the session gets expire after 30 min
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # calls everything we wrote.

oauth2 = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2), db: Session = Depends(get_db)):
    try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id = payload.get("user_id")
    except:
            raise HTTPException(status_code=401, detail="Invalid access")

    user = db.query(User).filter(User.id == user_id).first()
    if user is None:
            raise HTTPException(status_code=401, detail="User not found")

    return user
