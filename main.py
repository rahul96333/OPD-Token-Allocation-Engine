from fastapi import FastAPI
import uuid

app = FastAPI()

# 1. PRIORITY RULES (1 is highest, 5 is lowest)
PRIORITY_MAP = {
    "emergency": 1,
    "paid": 2,
    "followup": 3,
    "online": 4,
    "walkin": 5
}

# 2. DATA STORAGE (Temporary database in memory)
# We will create 3 doctors as required by the assignment
doctors_database = {
    "Dr. Sharma": {"capacity": 3, "current_queue": [], "overflow": []},
    "Dr. Reddy": {"capacity": 3, "current_queue": [], "overflow": []},
    "Dr. Kapoor": {"capacity": 3, "current_queue": [], "overflow": []}
}

@app.get("/")
def home():
    return {"message": "OPD Token Engine is Live"}

# 3. THE ALLOCATION ALGORITHM (The "Task" part of your assignment)
@app.post("/book-token")
def book_token(doctor_name: str, patient_name: str, source: str):
    if doctor_name not in doctors_database:
        return {"error": "Doctor not found"}

    doc = doctors_database[doctor_name]
    priority = PRIORITY_MAP.get(source.lower(), 5)
    
    new_patient = {
        "token_id": str(uuid.uuid4())[:8],
        "name": patient_name,
        "priority": priority,
        "source": source
    }

    # Case A: If slot has space (Hard Limit Enforcement)
    if len(doc["current_queue"]) < doc["capacity"]:
        doc["current_queue"].append(new_patient)
        return {"status": "Allocated", "patient": new_patient}

    # Case B: Slot is full - Check for Priority Reallocation
    else:
        # Find the lowest priority patient currently in the slot
        lowest_patient = max(doc["current_queue"], key=lambda x: x["priority"])

        if priority < lowest_patient["priority"]:
            # DYNAMIC REALLOCATION: Kick out the lower priority patient
            doc["current_queue"].remove(lowest_patient)
            doc["overflow"].append(lowest_patient)
            doc["current_queue"].append(new_patient)
            return {
                "status": "Priority Reallocation",
                "message": f"{patient_name} (Emergency/Paid) displaced {lowest_patient['name']}",
                "patient": new_patient
            }
        else:
            # Add to overflow (Waiting list)
            doc["overflow"].append(new_patient)
            return {"status": "Waiting List", "message": "Slot full, added to overflow", "patient": new_patient}

@app.get("/view-status")
def view_status():
    return doctors_database