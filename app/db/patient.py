from app.db.connection import db
patient_collection = db.get_collection("patient_collection")

async def add_patient(patient_data: dict)-> dict:
    patient = patient_collection.insert_one(patient_data)
    created_patient = patient_collection.find_one({"_id":patient.inserted_id})
    return created_patient
    

async def get_patient(id: str) -> dict:
    patient = patient_collection.find_one({"_id": id})
    if patient:
        return patient
    return None
    

async def get_patients() -> list:
    patients = []
    for patient in patient_collection.find():
        patients.append(patient)
    return patients


async def update_patient(id: str, update_patient_data: dict) -> dict:
    if len(update_patient_data) < 1:
        return False
    patient = patient_collection.find_one({"_id": id})
    if patient:
        patient_collection.update_one({"_id": id}, {"$set": update_patient_data})
        updated_patient = patient_collection.find_one({"_id": id})
        if updated_patient:
            return updated_patient
    return None


async def remove_patient(id: str) -> bool:
    patient = patient_collection.find_one({"_id": id})
    if patient:
        patient_collection.delete_one({"_id": id})
        return True
    return False


