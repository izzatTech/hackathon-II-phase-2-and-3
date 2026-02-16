"""
FastAPI backend for Todo application.
Provides /auth/login and /auth/register endpoints with CORS enabled.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uuid
import hashlib
import jwt
import datetime
from typing import Optional

# Initialize FastAPI app
app = FastAPI()

# Enable CORS for Next.js frontend (localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Secret key for JWT tokens - in production, use a strong secret from environment
SECRET_KEY = "your-super-secret-key-change-in-production"
ALGORITHM = "HS256"

# In-memory users store for testing
users = {}

# Pydantic models for request validation
class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def hash_password(password: str) -> str:
    """Hash a password for storing."""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a hashed password."""
    return hash_password(plain_password) == hashed_password

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    """Create a JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Auth endpoints with correct routes
@app.post("/auth/register")
async def register(user_data: UserCreate):
    if user_data.email in users:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store user with hashed password
    user_id = str(uuid.uuid4())
    hashed_pwd = hash_password(user_data.password)
    users[user_data.email] = {
        "id": user_id,
        "email": user_data.email,
        "username": user_data.username,
        "hashed_password": hashed_pwd
    }
    
    # Create token for auto-login
    access_token = create_access_token(data={"sub": user_data.email, "user_id": user_id})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user_id,
            "email": user_data.email,
            "username": user_data.username
        }
    }

@app.post("/auth/login")
async def login(login_data: LoginRequest):
    user = users.get(login_data.email)
    if not user or not verify_password(login_data.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    # Create token
    access_token = create_access_token(data={"sub": login_data.email, "user_id": user["id"]})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "username": user["username"]
        }
    }

# Optional: health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Todo API"}

# Optional: simple root endpoint
@app.get("/")
async def root():
    return {"message": "Todo backend is running!"}
