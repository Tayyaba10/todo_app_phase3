"""
Authentication module for handling JWT-based authentication
"""
from typing import Optional, Dict, Any
from fastapi import HTTPException, status
from ..utils.jwt_utils import create_access_token, verify_token
from datetime import timedelta


def authenticate_user(email: str, password: str) -> Optional[Dict[str, Any]]:
    """
    Authenticate a user with email and password.
    This is a placeholder implementation - in a real app, you'd check against a database.
    For now, we'll simulate authentication success for any non-empty credentials.
    """
    # In a real implementation, you would:
    # 1. Look up the user by email in the database
    # 2. Verify the password using a secure hash comparison
    # 3. Return user data if successful

    if not email or not password:
        return None

    # Placeholder: return a user-like object for demo purposes
    return {
        "id": 1,
        "email": email,
        "name": "Test User"
    }


def generate_auth_token(user_data: Dict[str, Any]) -> str:
    """
    Generate an authentication token for the given user data.
    """
    # Prepare the data to be stored in the JWT
    token_data = {
        "sub": str(user_data["id"]),  # subject (user ID)
        "email": user_data["email"],
        "name": user_data.get("name", ""),
    }

    # Create access token with default expiration
    access_token_expires = timedelta(minutes=30)
    token = create_access_token(
        data=token_data, expires_delta=access_token_expires
    )

    return token