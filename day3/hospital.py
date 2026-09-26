from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pymongo import MongoClient
from bson import ObjectId


# ============================================================
# APP
# ============================================================

app = FastAPI()


# ============================================================
# DB CONFIG
# ============================================================

URL = "mongodb://127.0.0.1:27017"

client = MongoClient(URL)

db = client["hospital_support_db"]

user_collection = db["users"]
request_collection = db["service_requests"]


# ============================================================
# USER SCHEMA
# ============================================================

class UserCreate(BaseModel):
    name: str
    email: str
    role: str
    department: str


class UserResponse(UserCreate):
    id: str


# ============================================================
# SERVICE REQUEST SCHEMA
# ============================================================

class ServiceRequestCreate(BaseModel):
    title: str
    description: str
    category: str
    status: str
    user: str


class ServiceRequestResponse(ServiceRequestCreate):
    id: str


# ============================================================
# USER HELPER
# ============================================================

def user_helper(user_doc):
    return {
        "id": str(user_doc["_id"]),
        "name": user_doc["name"],
        "email": user_doc["email"],
        "role": user_doc["role"],
        "department": user_doc["department"]
    }


# ============================================================
# SERVICE REQUEST HELPER
# ============================================================

def request_helper(request_doc):
    return {
        "id": str(request_doc["_id"]),
        "title": request_doc["title"],
        "description": request_doc["description"],
        "category": request_doc["category"],
        "status": request_doc["status"],
        "user": request_doc["user"]
    }


# ============================================================
# USER APIs - CRUD
# ============================================================


# CREATE USER
@app.post(
    "/users",
    status_code=201,
    response_model=UserResponse
)
def user_create(payload: UserCreate):

    user_dict = payload.model_dump()

    result = user_collection.insert_one(user_dict)

    new_user = user_collection.find_one(
        {"_id": result.inserted_id}
    )

    return user_helper(new_user)


# READ ALL USERS
@app.get(
    "/users",
    response_model=list[UserResponse]
)
def user_read_all():

    docs = user_collection.find()

    users = [
        user_helper(doc)
        for doc in docs
    ]

    return users


# READ USER BY ID
@app.get(
    "/users/{id}",
    response_model=UserResponse
)
def user_read_by_id(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid user ID",
            status_code=400
        )

    doc = user_collection.find_one(
        {"_id": ObjectId(id)}
    )

    if not doc:
        raise HTTPException(
            detail="User not found",
            status_code=404
        )

    return user_helper(doc)


# UPDATE USER
@app.put(
    "/users/{id}",
    response_model=UserResponse
)
def user_update(
    id: str,
    payload: UserCreate
):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid user ID",
            status_code=400
        )

    user_dict = payload.model_dump()

    result = user_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": user_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(
            detail="User not found",
            status_code=404
        )

    new_user = user_collection.find_one(
        {"_id": ObjectId(id)}
    )

    return user_helper(new_user)


# DELETE USER
@app.delete("/users/{id}")
def user_delete(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid user ID",
            status_code=400
        )

    result = user_collection.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            detail="User not found",
            status_code=404
        )

    return {
        "message": "User deleted successfully"
    }


# ============================================================
# SERVICE REQUEST APIs - CRUD
# ============================================================


# CREATE SERVICE REQUEST
@app.post(
    "/requests",
    status_code=201,
    response_model=ServiceRequestResponse
)
def request_create(
    payload: ServiceRequestCreate
):

    request_dict = payload.model_dump()

    result = request_collection.insert_one(
        request_dict
    )

    new_request = request_collection.find_one(
        {"_id": result.inserted_id}
    )

    return request_helper(new_request)


# READ ALL SERVICE REQUESTS
@app.get(
    "/requests",
    response_model=list[ServiceRequestResponse]
)
def request_read_all():

    docs = request_collection.find()

    requests = [
        request_helper(doc)
        for doc in docs
    ]

    return requests


# READ SERVICE REQUEST BY ID
@app.get(
    "/requests/{id}",
    response_model=ServiceRequestResponse
)
def request_read_by_id(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid request ID",
            status_code=400
        )

    doc = request_collection.find_one(
        {"_id": ObjectId(id)}
    )

    if not doc:
        raise HTTPException(
            detail="Service request not found",
            status_code=404
        )

    return request_helper(doc)


# UPDATE SERVICE REQUEST
@app.put(
    "/requests/{id}",
    response_model=ServiceRequestResponse
)
def request_update(
    id: str,
    payload: ServiceRequestCreate
):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid request ID",
            status_code=400
        )

    request_dict = payload.model_dump()

    result = request_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": request_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(
            detail="Service request not found",
            status_code=404
        )

    new_request = request_collection.find_one(
        {"_id": ObjectId(id)}
    )

    return request_helper(new_request)


# DELETE SERVICE REQUEST
@app.delete("/requests/{id}")
def request_delete(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid request ID",
            status_code=400
        )

    result = request_collection.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            detail="Service request not found",
            status_code=404
        )

    return {
        "message": "Service request deleted successfully"
    }