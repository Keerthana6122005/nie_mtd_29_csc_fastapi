from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from pymongo import MongoClient
from bson import ObjectId


# app
app = FastAPI()


# database config
URL = "mongodb://127.0.0.1:27017"
client = MongoClient(URL)

db = client["hospital_support_db"]
request_collection = db["support_requests"]


# schema - create request
class SupportRequestCreate(BaseModel):
    department: str
    request_type: str
    title: str
    description: str
    priority: str
    status: str


# schema - response
class SupportRequestResponse(SupportRequestCreate):
    id: str


# helper function
def request_helper(request_doc):
    return {
        "id": str(request_doc["_id"]),
        "department": request_doc["department"],
        "request_type": request_doc["request_type"],
        "title": request_doc["title"],
        "description": request_doc["description"],
        "priority": request_doc["priority"],
        "status": request_doc["status"]
    }


# HOME
@app.get("/")
def home():
    return {
        "message": "Hospital Support Request System"
    }


# CREATE REQUEST
@app.post("/requests", response_model=SupportRequestResponse)
def create_request(request: SupportRequestCreate):

    result = request_collection.insert_one(request.dict())

    new_request = request_collection.find_one(
        {"_id": result.inserted_id}
    )

    return request_helper(new_request)


# GET ALL REQUESTS
@app.get("/requests")
def get_all_requests():

    requests = request_collection.find()

    return [
        request_helper(request)
        for request in requests
    ]


# GET REQUEST BY ID
@app.get("/requests/{request_id}", response_model=SupportRequestResponse)
def get_request(request_id: str):

    if not ObjectId.is_valid(request_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    request = request_collection.find_one(
        {"_id": ObjectId(request_id)}
    )

    if request is None:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    return request_helper(request)


# UPDATE REQUEST
@app.put("/requests/{request_id}", response_model=SupportRequestResponse)
def update_request(
    request_id: str,
    request: SupportRequestCreate
):

    if not ObjectId.is_valid(request_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    result = request_collection.update_one(
        {"_id": ObjectId(request_id)},
        {
            "$set": request.dict()
        }
    )

    if result.matched_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    updated_request = request_collection.find_one(
        {"_id": ObjectId(request_id)}
    )

    return request_helper(updated_request)


# DELETE REQUEST
@app.delete("/requests/{request_id}")
def delete_request(request_id: str):

    if not ObjectId.is_valid(request_id):
        raise HTTPException(
            status_code=400,
            detail="Invalid request ID"
        )

    result = request_collection.delete_one(
        {"_id": ObjectId(request_id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=404,
            detail="Request not found"
        )

    return {
        "message": "Support request deleted successfully"
    }