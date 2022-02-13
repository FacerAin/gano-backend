from app.db.connection import db
room_collection = db.get_collection("room_collection")


async def add_room(room_data: dict) -> dict:
    room = room_collection.insert_one(room_data)
    created_room = room_collection.find_one({"_id": room.inserted_id})
    return created_room


async def get_room(id: str) -> dict:
    room = room_collection.find_one({"_id": id})
    if room:
        return room
    return None


async def get_rooms() -> list:
    rooms = []
    for room in room_collection.find():
        rooms.append(room)
    return rooms


async def update_room(id: str, update_room_data: dict) -> dict:
    if len(update_room_data) < 1:
        return False
    room = room_collection.find_one({"_id": id})
    if room:
        room_collection.update_one({"_id": id}, {"$set": update_room_data})
        updated_room = room_collection.find_one({"_id": id})
        if updated_room:
            return updated_room
    return None


async def remove_room(id: str) -> bool:
    room = room_collection.find_one({"_id": id})
    if room:
        room_collection.delete_one({"_id": id})
        return True
    return False
