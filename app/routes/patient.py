from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from app.db.patient import *
from app.models.patient import *

router = APIRouter()

@router.post("/", response_description="Add Patient Data", response_model=PatientSchema)
async def add_patient_data(patient_data: PatientSchema = Body(...)):
    patient_data = jsonable_encoder(patient_data)
    patient = await add_patient(patient_data)
    return patient


@router.get("/", response_description="Get All Patient Data", response_model=List[PatientSchema])
async def get_patients_data():
    patients = await get_patients()
    return patients


@router.get("/{id}", response_description="Get a Patient Data by id", response_model=PatientSchema)
async def get_patient_data_by_id(id: str):
    patient = await get_patient(id)
    if patient:
        return patient
    raise HTTPException(status_code=404, detail=f"Patient {id} not found")

@router.put("/", response_description="Update a Patient Data", response_model=PatientSchema)
async def update_patient_data(id: str, patient_data:UpdatePatientSchema = Body(...)):
    request = {key:value for key, value in patient_data.dict().items() if value is not None}
    patient = await update_patient(id, request)
    if patient:
        return patient
    raise HTTPException(status_code=404, detail=f"Patient {id} not found")


@router.delete("/", response_description="Remove a Patient Data")
async def remove_patient_data(id:str):
    result = await remove_patient(id)
    if result:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Patient {id} not found")
