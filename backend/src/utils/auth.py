"""
Authentication utilities for the Todo application.
Provides JWT token generation and verification functions.
"""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from passlib.context import CryptContext
import os

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Get secret key from environment or use a default (only for development)
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a plaintext password against a hashed password.

    Args:
        plain_password (str): Plaintext password to verify
        hashed_password (str): Hashed password to compare against

    Returns:
        bool: True if passwords match, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Generate a hash for a plaintext password.

    Args:
        password (str): Plaintext password to hash

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a JWT access token.

    Args:
        data (dict): Data to encode in the token
        expires_delta (Optional[timedelta]): Token expiration time delta

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str) -> Optional[dict]:
    """
    Verify a JWT access token and return its payload.

    Args:
        token (str): JWT token to verify

    Returns:
        Optional[dict]: Token payload if valid, None otherwise
    """
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        # Token has expired
        return None
    except jwt.JWTError:
        # Invalid token
        return None


def get_current_user_id(token: str) -> Optional[str]:
    """
    Extract user ID from a JWT token.

    Args:
        token (str): JWT token

    Returns:
        Optional[str]: User ID if token is valid, None otherwise
    """
    payload = verify_access_token(token)
    if payload:
        user_id = payload.get("sub")
        if user_id:
            return user_id
    return None