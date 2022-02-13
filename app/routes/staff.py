from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from app.db.staff import *
from app.models.staff import *
from app.util.auth import get_password_hash

router = APIRouter()


@router.post("/", response_description="Add Staff Data", response_model=StaffSchema)
async def add_staff_data(staff_data: StaffSchema = Body(...)):
    staff_data = jsonable_encoder(staff_data)
    staff_data["account_password"] = get_password_hash(
        staff_data["account_password"])
    staff = await add_staff(staff_data)
    return staff


@router.get("/", response_description="Get All Staff Data", response_model=List[StaffSchema])
async def get_staffs_data():
    staffs = await get_staffs()
    return staffs


@router.get("/{id}", response_description="Get a Staff Data by id", response_model=StaffSchema)
async def get_staff_data_by_id(id: str):
    staff = await get_staff(id)
    if staff:
        return staff
    raise HTTPException(status_code=404, detail=f"Staff {id} not found")


@router.put("/", response_description="Update a Staff Data", response_model=StaffSchema)
async def update_staff_data(id: str, staff_data: UpdateStaffSchema = Body(...)):
    request = {key: value for key, value in staff_data.dict().items()
               if value is not None}
    staff = await update_staff(id, request)
    if staff:
        return staff
    raise HTTPException(status_code=404, detail=f"Staff {id} not found")


@router.delete("/", response_description="Remove a Staff Data")
async def remove_staff_data(id: str):
    result = await remove_staff(id)
    if result:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Staff {id} not found")
