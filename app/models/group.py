from pydantic import BaseModel, Field
from typing import List, Optional
from app.util.PyObjectId import PyObjectId
from bson import ObjectId


class BedSchema(BaseModel):
    bed_no: int = Field(...)
    patient: PyObjectId = None


class RoomSchema(BaseModel):
    name: str = Field(...)
    bed_list: List[BedSchema] = None


class GroupSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    room_list: List[RoomSchema] = []
    staff_list: List[PyObjectId] = []

    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra: {
            "example": {
                "admission_reason": "독감"
            }
        }


class UpdateGroupSchema(BaseModel):
    patient_list: Optional[List[PyObjectId]]
    staff_list: Optional[List[PyObjectId]]


class AddStaffSchema(BaseModel):
    staff_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
