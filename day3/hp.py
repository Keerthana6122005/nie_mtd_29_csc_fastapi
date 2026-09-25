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


# -------------------------------------------------
# CREATE - Create a hospital support request
# -------------------------------------------------

@app.post(
    "/support-requests",
    status_code=201,
    response_model=SupportRequestResponse
)
def request_create(payload: SupportRequestCreate):

    request_dict = payload.model_dump()

    result = request_collection.insert_one(request_dict)

    new_request = request_collection.find_one(
        {"_id": result.inserted_id}
    )

    return request_helper(new_request)


# -------------------------------------------------
# READ ALL - Get all support requests
# -------------------------------------------------

@app.get(
    "/support-requests",
    response_model=list[SupportRequestResponse]
)
def request_read_all():

    docs = request_collection.find()

    requests = [
        request_helper(doc)
        for doc in docs
    ]

    return requests


# -------------------------------------------------
# READ BY ID - Get one support request
# -------------------------------------------------

@app.get(
    "/support-requests/{id}",
    response_model=SupportRequestResponse
)
def request_read_by_id(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid Support Request ID",
            status_code=400
        )

    doc = request_collection.find_one(
        {"_id": ObjectId(id)}
    )

    if not doc:
        raise HTTPException(
            detail="Support Request Not Found",
            status_code=404
        )

    return request_helper(doc)


# -------------------------------------------------
# UPDATE - Update a support request
# -------------------------------------------------

@app.put(
    "/support-requests/{id}",
    response_model=SupportRequestResponse
)
def request_update(
    id: str,
    payload: SupportRequestCreate
):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid Support Request ID",
            status_code=400
        )

    request_dict = payload.model_dump()

    result = request_collection.update_one(
        {"_id": ObjectId(id)},
        {"$set": request_dict}
    )

    if result.matched_count == 0:
        raise HTTPException(
            detail="Support Request Not Found",
            status_code=404
        )

    updated_request = request_collection.find_one(
        {"_id": ObjectId(id)}
    )

    return request_helper(updated_request)


# -------------------------------------------------
# DELETE - Delete a support request
# -------------------------------------------------

@app.delete("/support-requests/{id}")
def request_delete(id: str):

    if not ObjectId.is_valid(id):
        raise HTTPException(
            detail="Invalid Support Request ID",
            status_code=400
        )

    result = request_collection.delete_one(
        {"_id": ObjectId(id)}
    )

    if result.deleted_count == 0:
        raise HTTPException(
            detail="Support Request Not Found",
            status_code=404
        )

    return {
        "message": "Support Request Deleted Successfully"
    }