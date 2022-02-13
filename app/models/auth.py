from pydantic import BaseModel, Field
from typing import List, Optional
from app.util.PyObjectId import PyObjectId
from bson import ObjectId


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    account_id: Optional[str] = None

class LoginScema(BaseModel):
    account_id: str = Field(...)
    account_password: str = Field(...)
