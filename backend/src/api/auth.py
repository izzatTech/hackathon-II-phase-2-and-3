"""
Authentication API endpoints for the Todo application.
Provides endpoints for user registration, login, logout, and profile management.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import Optional
from backend.src.models.user import User
from backend.src.schemas.user import UserCreate, UserResponse, Token, UserProfile
from backend.src.repositories.user_repository import UserRepository
from backend.src.services.auth_service import AuthService
from backend.src.services.session_service import SessionService
from backend.src.middleware.auth import require_authentication
from backend.src.config.database import get_session
import uuid


router = APIRouter(prefix="/auth", tags=["authentication"])


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, db: Session = Depends(get_session)):
    """
    Register a new user.

    Args:
        user_data (UserCreate): User registration data
        db (Session): Database session

    Returns:
        UserResponse: The created user information

    Raises:
        HTTPException: If user with email/username already exists
    """
    user_repo = UserRepository(db)
    session_service = SessionService(db)
    auth_service = AuthService(db, user_repo, session_service)

    created_user = auth_service.register_user(
        email=user_data.email,
        username=user_data.username,
        password=user_data.password
    )

    if not created_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )

    return UserResponse.from_orm(created_user)


@router.post("/login", response_model=Token)
def login(email: str, password: str, db: Session = Depends(get_session)):
    """
    Authenticate a user and return an access token.

    Args:
        email (str): User's email address
        password (str): User's password
        db (Session): Database session

    Returns:
        Token: Access token and token type

    Raises:
        HTTPException: If authentication fails
    """
    user_repo = UserRepository(db)
    session_service = SessionService(db)
    auth_service = AuthService(db, user_repo, session_service)

    token_data = auth_service.login_user(email, password)

    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return Token(access_token=token_data["access_token"], token_type=token_data["token_type"])


@router.post("/logout")
def logout(current_user_id: str = Depends(require_authentication), db: Session = Depends(get_session)):
    """
    Logout the current user.

    Args:
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        dict: Success message
    """
    user_repo = UserRepository(db)
    session_service = SessionService(db)
    auth_service = AuthService(db, user_repo, session_service)

    success = auth_service.logout_user(current_user_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Logout failed"
        )

    return {"message": "Successfully logged out"}


@router.get("/profile", response_model=UserProfile)
def get_profile(current_user_id: str = Depends(require_authentication), db: Session = Depends(get_session)):
    """
    Get the profile of the current authenticated user.

    Args:
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        UserProfile: Current user's profile information
    """
    user_repo = UserRepository(db)

    user = user_repo.get_user_by_id(uuid.UUID(current_user_id))

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return UserProfile(
        id=user.id,
        email=user.email,
        username=user.username,
        created_at=user.created_at
    )


@router.put("/profile", response_model=UserProfile)
def update_profile(
    user_data: UserCreate,  # For simplicity, reuse UserCreate for update (in real app use separate schema)
    current_user_id: str = Depends(require_authentication),
    db: Session = Depends(get_session)
):
    """
    Update the profile of the current authenticated user.

    Args:
        user_data (UserCreate): Updated user data
        current_user_id (str): ID of the current authenticated user
        db (Session): Database session

    Returns:
        UserProfile: Updated user's profile information
    """
    user_repo = UserRepository(db)

    # Get the current user
    current_user = user_repo.get_user_by_id(uuid.UUID(current_user_id))

    if not current_user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # Prepare update data (excluding password and other non-profile fields)
    update_data = {}
    if user_data.email and user_data.email != current_user.email:
        # Check if new email is already taken by another user
        existing_user = user_repo.get_user_by_email(user_data.email)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already in use by another user"
            )
        update_data['email'] = user_data.email

    if user_data.username and user_data.username != current_user.username:
        # Check if new username is already taken by another user
        existing_user = user_repo.get_user_by_username(user_data.username)
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Username already in use by another user"
            )
        update_data['username'] = user_data.username

    # Update the user
    updated_user = user_repo.update_user(uuid.UUID(current_user_id), update_data)

    if not updated_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to update user profile"
        )

    return UserProfile(
        id=updated_user.id,
        email=updated_user.email,
        username=updated_user.username,
        created_at=updated_user.created_at
    )