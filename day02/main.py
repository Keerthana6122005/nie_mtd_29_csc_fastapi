from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
app = FastAPI()
@app.get("/")
def home():
    return{"message" : "Enterprise IT Service Desk - server"}
db = {
    1 : {"id" : 1,"tittle" : "computer is not on",
        "description" : "power is not working",
         "category" : "Hardware","status" : "NEW"},
    2 : {"id" : 2,"tittle" : "internet is not working",
         "description" : "wify problem",
         "category" : "Hardware","status" : "NEW"}
    }
#Schemes
class TicketCreate(BaseModel):
    title : str
    description : str
    category :str
    status : str
class TicketResponse(TicketCreate): 
    id : int 
#APIs 
@app.get("/tickets")
def get_tickets():
    return list(db.values())

    
@app.get("/tickets/{id}")
def get_tickets(id: int):
    if id not in db:
        raise HTTPException(status_code=404,detail="Ticket not found")
    return db[id]



@app.post("/tickets", status_code=201,response_model=TicketResponse)
def ticket_create(ticket_payload : TicketCreate):
    new_id = max(db.keys(), default=0) + 1
    db[new_id] = {"id" : new_id, **ticket_payload.model_dump()}
    return db[new_id]

@app.put("/tickets/{id}", response_model=TicketResponse)
def tickets_update(id: int,ticket_payload: TicketCreate):
    if id not in db:
        raise HTTPException(detail="Ticket not found", status_code=404)
    db[id] = {"id" : id , **ticket_payload.model_dump()}
    return db[id]

@app.delete("/tickets/{id}")
def tickets_delete(id: int):
    if id not in db:
        raise HTTPException(detail="Ticket not found",status_code=404)
    del db[id]
    return {"message" : "Ticket deleted successfully"} 

