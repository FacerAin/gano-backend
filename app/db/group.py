from app.db.connection import db
group_collection = db.get_collection("group_collection")

async def add_group(group_data: dict) -> dict:
    group = group_collection.insert_one(group_data)
    created_group = group_collection.find_one({"_id": group.inserted_id})
    return created_group


async def get_group(id: str) -> dict:
    group = group_collection.find_one({"_id": id})
    if group:
        return group
    return None


async def get_groups() -> list:
    groups = []
    for group in group_collection.find():
        groups.append(group)
    return groups


async def update_group(id: str, update_group_data: dict) -> dict:
    if len(update_group_data) < 1:
        return False
    group = group_collection.find_one({"_id": id})
    if group:
        group_collection.update_one({"_id": id}, {"$set": update_group_data})
        updated_group = group_collection.find_one({"_id": id})
        if updated_group:
            return updated_group
    return None


async def remove_group(id: str) -> bool:
    group = group_collection.find_one({"_id": id})
    if group:
        group_collection.delete_one({"_id": id})
        return True
    return False
