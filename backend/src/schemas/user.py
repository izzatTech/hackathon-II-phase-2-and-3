"""
User schemas for the Todo application.
Defines Pydantic models for User API requests and responses.
"""

from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import uuid


class UserBase(BaseModel):
    """Base schema for User with shared attributes."""
    email: str
    username: str


class UserCreate(UserBase):
    """Schema for creating a new user."""
    password: str


class UserUpdate(BaseModel):
    """Schema for updating an existing user."""
    email: Optional[str] = None
    username: Optional[str] = None


class UserResponse(UserBase):
    """Schema for user response with additional fields."""
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class UserProfile(UserBase):
    """Schema for user profile information."""
    id: uuid.UUID
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for authentication token."""
    access_token: str
    token_type: str


class TokenData(BaseModel):
    """Schema for token data."""
    username: Optional[str] = None