# pyright: reportMissingImports=false
import os
from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

# ---------- Configuration (use environment variables in production) ----------
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-this-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

# ---------- Password hashing context ----------
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ---------- OAuth2 scheme (token URL must match your login endpoint) ----------
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")   # Adjust if your login endpoint is different

# ---------- Pydantic models for token ----------
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

# ---------- Password helpers ----------
def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

# ---------- JWT helpers ----------
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str) -> TokenData:
    """
    Decode and validate the JWT token.
    Returns TokenData (username) or raises HTTPException.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    return token_data

# ---------- Dependency: get current user ----------
# This assumes you have a User model/CRUD. Adjust the import and logic to match your project.
# For demonstration, we'll use a dummy user retrieval.
# Replace this with actual database lookup.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Extract and validate the token, then return the user object.
    """
    token_data = verify_token(token)
    # ---- Replace the following dummy logic with your real database fetch ----
    # Example: user = await get_user_by_username(token_data.username)
    # If user is None, raise HTTPException(404, "User not found")
    # Return the user object (or a dict) that your routes expect.
    user = {"username": token_data.username}   # dummy
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Optional: if you have a real user model, you can use this signature:
# async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
#     ...