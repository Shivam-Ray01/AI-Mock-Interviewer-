from dotenv import load_dotenv
import bcrypt
import os
import jwt
from datetime import datetime, timezone, timedelta

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

