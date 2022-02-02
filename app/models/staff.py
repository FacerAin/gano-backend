from pydantic import BaseModel, Field
from typing import List, Optional
from app.util.PyObjectId import PyObjectId
from bson import ObjectId


class StaffSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    account_id: str = Field(...)
    account_password: str = Field(...)
    group: PyObjectId = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra: {
            "example": {
                "name": "홍길동",
                "account_id": "abc1234",
                "account_password": "123456789"
            }
        }


class UpdateStaffSchema(BaseModel):
    name: Optional[str]
    account_id: Optional[str]
    account_password: Optional[str]
    group: Optional[PyObjectId]

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra: {
            "example": {
                "name": "홍길동",
                "account_id": "abc1234",
                "account_password": "123456789"
            }
        }
