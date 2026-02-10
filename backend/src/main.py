"""
FastAPI backend for Todo application.
Provides /login and /signup endpoints with CORS enabled.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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

# Pydantic models for request validation
class SignupRequest(BaseModel):
    email: str
    username: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

# In-memory users store for testing
users = {}

# Signup endpoint
@app.post("/signup")
async def signup(data: SignupRequest):
    if data.email in users:
        return {"success": False, "error": "Email already exists"}
    users[data.email] = {"username": data.username, "password": data.password}
    return {"success": True, "user": {"email": data.email, "username": data.username}}

# Login endpoint
@app.post("/login")
async def login(data: LoginRequest):
    user = users.get(data.email)
    if not user or user["password"] != data.password:
        return {"success": False, "error": "Invalid credentials"}
    return {"success": True, "user": {"email": data.email, "username": user["username"]}}

# Optional: simple root endpoint
@app.get("/")
async def root():
    return {"message": "Todo backend is running!"}
