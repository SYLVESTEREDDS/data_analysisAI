# Neurolytix\backend\models\user_model.py

from pydantic import BaseModel, EmailStr

class User(BaseModel):
    id: str
    username: str
    email: EmailStr
    password: str
