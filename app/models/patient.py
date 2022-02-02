from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional
from app.util.PyObjectId import PyObjectId
from bson import ObjectId


class RecordSchema(BaseModel):
    vital: int = 1
    blood_text: int = 1


class PatientSchema(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = "Patient"
    admission_date: str = Field(...)
    admission_reason: str = Field(...)
    attending_physician: str = Field(...)
    past_history: List[str] = Field(...)
    diagnosis: List[str] = Field(...)
    allergy: List[str] = Field(...)
    operation_history: List[str] = Field(...)
    record: List[RecordSchema] = []

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


class UpdatePatientSchema(BaseModel):
    name: Optional[str]
    admission_date: Optional[str]
    admission_reason: Optional[str]
    attending_physician: Optional[str]
    past_history: Optional[List[str]]
    diagnosis: Optional[List[str]]
    allergy: Optional[List[str]]
    operation_history: Optional[List[str]]
    record: Optional[List[RecordSchema]]

    class Config:
        json_encoders = {ObjectId: str}
        arbitrary_types_allowed = True
        schema_extra: {
            "example": {
                "name": "홍길동",
                "admission_reason": "독감"
            }
        }
