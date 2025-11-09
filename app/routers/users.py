"""
Users Router - User Authentication Endpoints

FastAPI endpoints for user authentication:
- Register new users
- Login and get JWT tokens

These endpoints handle user authentication for the RAG Chat Backend.
"""

from fastapi import APIRouter, HTTPException, status
from app.models.schemas import UserRegister, UserLogin, TokenResponse
from app.services import AuthService
from app.database import UsersRepository

# Create router with prefix and tags
router = APIRouter(
    prefix="/api/v1/users",
    tags=["users"]
)

# Initialize services and repositories
auth_service = AuthService()
users_repo = UsersRepository()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: UserRegister) -> dict:
    """
    Register a new user.

    This endpoint:
    1. Validates the email format and password strength
    2. Checks if user already exists
    3. Hashes the password using bcrypt
    4. Saves user to database
    5. Returns success message

    Args:
        user_data: UserRegister model with email, password, and name

    Returns:
        Dict with success message

    Raises:
        HTTPException 400: If user already exists
        HTTPException 500: If registration fails
    """
    try:
        # Hash the password before storing
        hashed_password = auth_service.hash_password(user_data.password)

        # Create user in database
        user = await users_repo.create_user(
            email=user_data.email,
            name=user_data.name,
            hashed_password=hashed_password
        )

        return {
            "success": True,
            "message": "User registered successfully",
            "user": {
                "id": user["id"],
                "email": user["email"],
                "name": user["name"]
            }
        }

    except Exception as e:
        error_message = str(e)
        # Check if it's a duplicate user error
        if "already exists" in error_message:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists"
            )
        # General error
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {error_message}"
        )


@router.post("/login")
async def login_user(credentials: UserLogin) -> TokenResponse:
    """
    Login user and return JWT access token.

    This endpoint:
    1. Finds user by email
    2. Verifies password against stored hash
    3. Generates JWT access token
    4. Returns token and user info

    Args:
        credentials: UserLogin model with email and password

    Returns:
        TokenResponse with access_token, token_type, and user info

    Raises:
        HTTPException 401: If credentials are invalid
        HTTPException 500: If login process fails
    """
    try:
        # Get user from database
        user = await users_repo.get_user_by_email(credentials.email)

        # Check if user exists
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Verify password
        if not auth_service.verify_password(credentials.password, user["password"]):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password"
            )

        # Create JWT access token
        access_token = auth_service.create_access_token({
            "id": user["id"],
            "email": user["email"],
            "name": user["name"]
        })

        # Return token and user info
        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user["id"],
                "email": user["email"],
                "name": user["name"]
            }
        )

    except HTTPException:
        # Re-raise HTTP exceptions (401, etc.)
        raise
    except Exception as e:
        # Handle unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Login failed: {str(e)}"
        )
