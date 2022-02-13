from app.db.connection import db
staff_collection = db.get_collection("staff_collection")

async def add_staff(staff_data: dict)-> dict:
    staff = staff_collection.insert_one(staff_data)
    created_staff = staff_collection.find_one({"_id":staff.inserted_id})
    return created_staff
    

async def get_staff(id: str) -> dict:
    staff = staff_collection.find_one({"_id": id})
    if staff:
        return staff
    return None
    
async def get_staff_by_account_id(account_id: str)->dict:
    staff = staff_collection.find_one({"account_id": account_id})
    if staff:
        return staff
    return None


async def get_staffs() -> list:
    staffs = []
    for staff in staff_collection.find():
        staffs.append(staff)
    return staffs


async def update_staff(id: str, update_staff_data: dict) -> dict:
    if len(update_staff_data) < 1:
        return False
    staff = staff_collection.find_one({"_id": id})
    if staff:
        staff_collection.update_one({"_id": id}, {"$set": update_staff_data})
        updated_staff = staff_collection.find_one({"_id": id})
        if updated_staff:
            return updated_staff
    return None


async def remove_staff(id: str) -> bool:
    staff = staff_collection.find_one({"_id": id})
    if staff:
        staff_collection.delete_one({"_id": id})
        return True
    return False

