# backend/app/auth.py
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

router = APIRouter()

# ===== Password Hashing =====
pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__truncate_error=True,  # Allow truncation
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# ===== JWT Settings =====
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ===== Pydantic Models =====
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    
    @validator('password')
    def validate_password(cls, v):
        # Check minimum length
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check maximum length (bcrypt limit)
        if len(v) > 72:
            raise ValueError('Password must be 72 characters or less')
        
        return v

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class UserResponse(BaseModel):
    email: str
    name: str
    created_at: Optional[datetime] = None

# ===== Mock Database =====
users_db = {}

# ===== Helper Functions =====
def verify_password(plain_password, hashed_password):
    """Verify a plain password against a hashed password"""
    try:
        return pwd_context.verify(plain_password, hashed_password)
    except Exception as e:
        print(f"Password verification error: {e}")
        return False

def get_password_hash(password):
    """Hash a password using bcrypt"""
    try:
        # Truncate password if it's too long (with warning)
        if len(password) > 72:
            print(f"⚠️ Password truncated from {len(password)} to 72 characters")
            password = password[:72]
        
        return pwd_context.hash(password)
    except Exception as e:
        print(f"Password hashing error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error during password processing"
        )

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a JWT access token"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# ===== Routes =====

@router.post("/register")
async def register(user: UserCreate):
    try:
        print(f"📝 Registration: {user.email}")
        print(f"📝 Password length: {len(user.password)}")
        
        # Check if user exists
        if user.email in users_db:
            print(f"❌ Email already registered: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        
        # Hash password
        try:
            hashed_password = get_password_hash(user.password)
            print(f"✅ Password hashed for: {user.email}")
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Password error: {str(e)}"
            )
        
        # Create user
        users_db[user.email] = {
            "email": user.email,
            "name": user.name,
            "password": hashed_password,
            "created_at": datetime.utcnow()
        }
        print(f"✅ User created: {user.email}")
        print(f"📊 Total users: {len(users_db)}")
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "name": user.name
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Registration error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )

@router.post("/login")
async def login(user: UserLogin):
    try:
        print(f"🔐 Login: {user.email}")
        
        # Check if user exists
        if user.email not in users_db:
            print(f"❌ User not found: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        db_user = users_db[user.email]
        
        # Verify password
        if not verify_password(user.password, db_user["password"]):
            print(f"❌ Invalid password: {user.email}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )
        
        print(f"✅ Login successful: {user.email}")
        
        # Create access token
        access_token = create_access_token(data={"sub": user.email})
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "name": db_user["name"]
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Login error: {e}")
        print(traceback.format_exc())
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}

@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    if email not in users_db:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    db_user = users_db[email]
    return {
        "email": db_user["email"],
        "name": db_user["name"],
        "created_at": db_user["created_at"]
    }