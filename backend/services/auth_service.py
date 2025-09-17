# Neurolytix\backend\services\auth_service.py

from models.user_model import User
from passlib.context import CryptContext
import jwt
import time

SECRET_KEY = "SUPER_SECRET_NEUROLYTIX_KEY"  # Replace with env var in production
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_SECONDS = 3600  # 1 hour

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class AuthService:
    """
    Handles user authentication, signup, and JWT token generation.
    """

    def __init__(self):
        # In-memory user store (replace with DB in production)
        self.users = {}

    def create_user(self, username: str, email: str, password: str):
        if username in self.users:
            raise ValueError("Username already exists.")
        hashed_password = pwd_context.hash(password)
        user_id = str(len(self.users) + 1)
        self.users[username] = {"id": user_id, "username": username, "email": email, "password": hashed_password}
        return self.users[username]

    def authenticate_user(self, username: str, password: str):
        user = self.users.get(username)
        if not user:
            raise ValueError("Invalid username or password.")
        if not pwd_context.verify(password, user["password"]):
            raise ValueError("Invalid username or password.")
        token = self.create_access_token({"sub": username})
        return token

    def create_access_token(self, data: dict):
        payload = data.copy()
        payload.update({"exp": time.time() + ACCESS_TOKEN_EXPIRE_SECONDS})
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token
