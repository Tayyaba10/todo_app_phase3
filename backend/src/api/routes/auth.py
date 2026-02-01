import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from ...models.user import User, UserRead
from ...core.auth import authenticate_user, generate_auth_token
from ...core.database import get_session
from ...utils.jwt_utils import create_access_token
from ...api.deps import get_current_user
from ..schemas.auth import RegisterRequest, RegisterResponse, LoginRequest, LoginResponse, ProfileResponse
from datetime import timedelta
from typing import Optional
from datetime import datetime
import json


# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


router = APIRouter()


@router.post("/register", response_model=RegisterResponse)
def register(
    register_data: RegisterRequest,
    session: Session = Depends(get_session)
):
    """
    Register a new user.
    """
    logger.info(f"Registering user with email: {register_data.email}")

    # Check if user already exists
    existing_user = session.query(User).filter(User.email == register_data.email).first()
    if existing_user:
        logger.warning(f"Registration attempted for existing email: {register_data.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exists"
        )

    # In a real application, you would hash the password before storing it
    # For now, we'll simulate user creation
    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    raw_password = register_data.password.strip()

    if len(raw_password.encode("utf-8")) > 72:
        raise HTTPException(
            status_code=400,
            detail="Password must be 72 characters or fewer"
        )
    hashed_password = pwd_context.hash(raw_password)

    # Create new user
    user = User(
        email=register_data.email,
        name=register_data.name,
        hashed_password=hashed_password
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Generate authentication token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.name or ""
    }
    token = create_access_token(data=token_data)

    logger.info(f"Successfully registered user with ID: {user.id}")
    return RegisterResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        created_at=user.created_at,
        token=token
    )


@router.post("/login", response_model=LoginResponse)
def login(
    login_data: LoginRequest,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token.
    """
    logger.info(f"Login attempt for user: {login_data.email}")

    # In a real application, you would verify the credentials against the database
    # For now, we'll simulate authentication
    user = session.query(User).filter(User.email == login_data.email).first()

    if not user:
        logger.warning(f"Failed login attempt for non-existent user: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    from passlib.context import CryptContext
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # Verify the password hash
    if not pwd_context.verify(login_data.password, user.hashed_password):
        logger.warning(f"Failed login attempt with incorrect password for user: {login_data.email}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate authentication token
    token_data = {
        "sub": str(user.id),
        "email": user.email,
        "name": user.name or ""
    }
    token = create_access_token(data=token_data)

    logger.info(f"Successful login for user ID: {user.id}")
    return LoginResponse(
        user_id=user.id,
        email=user.email,
        name=user.name,
        token=token
    )


@router.get("/profile", response_model=ProfileResponse)
def get_profile(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get the authenticated user's profile.
    """
    logger.info(f"Retrieving profile for user ID: {current_user['user_id']}")

    # Fetch the user from the database using the ID from the token
    user_id = current_user["user_id"]
    user = session.get(User, user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return ProfileResponse(
        id=user.id,
        email=user.email,
        name=user.name or "",
        created_at=user.created_at,
        updated_at=user.updated_at
    )