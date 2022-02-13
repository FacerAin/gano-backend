from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from app.db.room import *
from app.models.room import *
from app.db.staff import get_staff, update_staff
from app.db.patient import get_patient
router = APIRouter()


@router.get("/", response_description="Get All Room Data", response_model=List[RoomSchema])
async def get_rooms_data():
    rooms = await get_rooms()
    return rooms


@router.post("/", response_description="Create a Room", response_model=RoomSchema)
async def create_room_data(create_room_data: CreateRoomSchema = Body(...)):
    bed_num = create_room_data.bed_num
    room_name = create_room_data.name
    bed_list = []
    for i in range(bed_num):
        bed_list.append(BedSchema(bed_no=i+1))
    room_data = RoomSchema(name=room_name, bed_list=bed_list)
    room = await add_room(jsonable_encoder(room_data))
    return room


@router.delete("/", response_description="Remove a Room by id")
async def remove_room_data(id: str):
    result = await remove_room(id)
    if result:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Room {id} not found")


@router.put("/{room_id}/patient/{patient_id}", response_description="Add a patient in Room by room id")
async def add_patient_data(room_id: str, patient_id: str, add_patient_data: AddPatientSchema = Body(...)):
    bed_no = add_patient_data.bed_no
    room = await get_room(room_id)
    patient = await get_patient(patient_id)

    if not room:
        raise HTTPException(
            status_code=404, detail=f"Room {room_id} not found")

    if not patient:
        raise HTTPException(
            status_code=404, detail=f"Patient {patient_id} not found")

    if bed_no < 1 or len(room['bed_list']) < bed_no:
        raise HTTPException(
            status_code=404, detail=f"Bed_no {bed_no} not found")

    room['bed_list'][bed_no - 1]['patient'] = patient_id
    updated_room = await update_room(room_id, room)
    return updated_room


@router.delete("/{room_id}/patient/{patient_id}", response_description="Remove a patient in Room by room id")
async def add_patient_data(room_id: str, patient_id: str, add_patient_data: AddPatientSchema = Body(...)):
    bed_no = add_patient_data.bed_no
    room = await get_room(room_id)
    patient = await get_patient(patient_id)

    if not room:
        raise HTTPException(
            status_code=404, detail=f"Room {room_id} not found")

    if not patient:
        raise HTTPException(
            status_code=404, detail=f"Patient {patient_id} not found")

    if bed_no < 1 or len(room['bed_list']) < bed_no:
        raise HTTPException(
            status_code=404, detail=f"Bed_no {bed_no} not found")

    room['bed_list'][bed_no - 1]['patient'] = None
    updated_room = await update_room(room_id, room)
    return updated_room
