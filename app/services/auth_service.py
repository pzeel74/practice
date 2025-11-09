"""
Authentication Service

Handles password hashing, verification, and JWT token generation/validation.

Key Features:
- Bcrypt password hashing (secure one-way encryption)
- JWT token generation with expiration
- Token verification and decoding
"""

from datetime import datetime, timedelta
from typing import Optional, Dict
import bcrypt
import jwt
import os
from dotenv import load_dotenv

load_dotenv()


class AuthService:
    """Service for authentication operations."""

    def __init__(self):
        """Initialize authentication service with JWT secret."""
        # Get SECRET_KEY from environment or use default for development
        # In production, this should be a strong random string
        self.SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key-change-in-production")
        self.ALGORITHM = "HS256"  # Standard algorithm for JWT
        self.ACCESS_TOKEN_EXPIRE_DAYS = 30  # Token valid for 30 days

    def hash_password(self, password: str) -> str:
        """
        Hash a password using bcrypt.

        Bcrypt automatically:
        - Generates a random salt (makes each hash unique)
        - Uses multiple rounds of hashing (slow = harder to crack)

        Args:
            password: Plain text password

        Returns:
            Hashed password as string (safe to store in database)
        """
        # Convert password to bytes
        password_bytes = password.encode('utf-8')

        # Generate salt and hash password
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password_bytes, salt)

        # Return as string for database storage
        return hashed.decode('utf-8')

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify a password against its hash.

        Args:
            plain_password: Password provided by user during login
            hashed_password: Hashed password from database

        Returns:
            True if password matches, False otherwise
        """
        password_bytes = plain_password.encode('utf-8')
        hashed_bytes = hashed_password.encode('utf-8')

        return bcrypt.checkpw(password_bytes, hashed_bytes)

    def create_access_token(self, user_data: Dict) -> str:
        """
        Create a JWT access token.

        The token contains:
        - user_id: For identifying the user
        - email: For displaying user info
        - exp: Expiration timestamp

        Args:
            user_data: Dictionary with user information (id, email, name)

        Returns:
            JWT token as string
        """
        # Calculate expiration time
        expire = datetime.utcnow() + timedelta(days=self.ACCESS_TOKEN_EXPIRE_DAYS)

        # Create token payload (data to encode)
        payload = {
            "user_id": user_data["id"],
            "email": user_data["email"],
            "name": user_data["name"],
            "exp": expire  # Expiration time
        }

        # Encode and return JWT token
        token = jwt.encode(payload, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return token

    def verify_token(self, token: str) -> Optional[Dict]:
        """
        Verify and decode a JWT token.

        Args:
            token: JWT token string

        Returns:
            Decoded token payload if valid, None if invalid/expired
        """
        try:
            # Decode and verify token
            payload = jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            # Token has expired
            return None
        except jwt.InvalidTokenError:
            # Token is invalid
            return None
