# Neurolytix\backend\routers\auth.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import JSONResponse
from services.auth_service import AuthService
from models.user_model import User
from pydantic import BaseModel

router = APIRouter()

auth_service = AuthService()


class SignupRequest(BaseModel):
    username: str
    email: str
    password: str


@router.post("/signup")
def signup(request: SignupRequest):
    """
    Register a new user.
    """
    try:
        user = auth_service.create_user(request.username, request.email, request.password)
        return JSONResponse(
            status_code=201,
            content={"message": "User registered successfully.", "user_id": user["id"]}
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Login a user and return JWT token.
    """
    try:
        token = auth_service.authenticate_user(form_data.username, form_data.password)
        return {"access_token": token, "token_type": "bearer"}
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
