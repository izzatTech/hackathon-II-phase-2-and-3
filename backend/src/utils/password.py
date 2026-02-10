"""
Password utilities for the Todo application.
Provides functions for hashing and verifying passwords.
"""

from passlib.context import CryptContext

# Initialize password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


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