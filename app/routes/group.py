from fastapi import APIRouter, Body, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from typing import List
from app.db.group import *
from app.models.group import *
from app.db.staff import get_staff, update_staff
from app.db.room import get_room
router = APIRouter()


@router.post("/", response_description="Add group Data", response_model=GroupSchema)
async def add_group_data(group_data: GroupSchema = Body(...)):
    group_data = jsonable_encoder(group_data)
    group = await add_group(group_data)
    return group


@router.get("/", response_description="Get All group Data", response_model=List[GroupSchema])
async def get_groups_data():
    groups = await get_groups()
    return groups


@router.get("/{id}", response_description="Get a group Data by id", response_model=GroupSchema)
async def get_group_data_by_id(id: str):
    group = await get_group(id)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"group {id} not found")


@router.put("/", response_description="Update a group Data", response_model=GroupSchema)
async def update_group_data(id: str, group_data: UpdateGroupSchema = Body(...)):
    request = {key: value for key, value in group_data.dict().items()
               if value is not None}
    group = await update_group(id, request)
    if group:
        return group
    raise HTTPException(status_code=404, detail=f"group {id} not found")


@router.delete("/", response_description="Remove a group Data")
async def remove_group_data(id: str):
    result = await remove_group(id)
    if result:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"group {id} not found")


@router.put("/{group_id}/staff/{staff_id}", response_description="Add a Staff in Group by id")
async def add_staff_data(group_id: str, staff_id: str):
    group = await get_group(group_id)
    staff = await get_staff(staff_id)
    if not group:
        raise HTTPException(
            status_code=404, detail=f"Group {group_id} not found")

    if not staff:
        raise HTTPException(
            status_code=404, detail=f"Staff {staff_id} not found")

    group_set = set(group['staff_list'])
    group_set.add(staff_id)
    group['staff_list'] = list(group_set)

    staff['group'] = group_id

    updated_group = await update_group(group_id, group)
    updated_staff = await update_staff(staff_id, staff)
    return updated_group


@router.put("/{group_id}/room/{room_id}", response_description="Add a Room in Group by id")
async def add_room_data(group_id: str, room_id: str):
    group = await get_group(group_id)
    room = await get_room(room_id)
    if not group:
        raise HTTPException(
            status_code=404, detail=f"Group {group_id} not found")

    if not room:
        raise HTTPException(
            status_code=404, detail=f"Room {room_id} not found")

    room_set = set(group['room_list'])
    room_set.add(room_id)
    group['room_list'] = list(room_set)
    updated_group = await update_group(group_id, group)

    return updated_group
