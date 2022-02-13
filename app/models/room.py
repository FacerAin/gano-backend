from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from app.util.PyObjectId import PyObjectId
from bson import ObjectId


class BedSchema(BaseModel):
    bed_no: int = Field(...)
    patient: PyObjectId = None


class RoomSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    bed_list: List[BedSchema] = None

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra: {
            "example": {
                "name": "홍길동",
                "admission_reason": "독감"
            }
        }


class UpdateRoomSchema(BaseModel):
    bed_list: Optional[List[PyObjectId]]
    name: Optional[str]


class CreateRoomSchema(BaseModel):
    name: str = Field(...)
    bed_num: int = Field(...)


class AddPatientSchema(BaseModel):
    bed_no: int = Field(...)
