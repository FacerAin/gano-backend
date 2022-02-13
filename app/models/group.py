from pydantic import BaseModel, Field
from typing import List, Optional
from app.util.PyObjectId import PyObjectId
from bson import ObjectId

class GroupSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    room_list: List[PyObjectId] = []
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
    room_list: Optional[List[PyObjectId]]
    staff_list: Optional[List[PyObjectId]]


class AddStaffSchema(BaseModel):
    staff_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
