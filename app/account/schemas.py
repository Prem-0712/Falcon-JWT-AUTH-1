from datetime import datetime

from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Literal


class UserRegisterReq(BaseModel):
    name: str
    email: EmailStr
    password: str
    password2: str
    user_role: Literal["customer", "seller"] = "customer"


class UserRegisterRes(BaseModel):
    msg: str


class JWT_Token(BaseModel):
    access_token: str
    refresh_token: str


class UserLoginReq(BaseModel):
    email: EmailStr
    password: str


class UserLoginRes(BaseModel):
    msg: str
    user_role: Literal["customer", "seller"]
    jwt_tokens: JWT_Token


class UserProfileRes(BaseModel):

    model_config = ConfigDict(from_attributes=True)
    
    id: int
    name: str
    email: EmailStr
    is_customer: bool
    is_seller: bool
    created_at: datetime
    updated_at: datetime
