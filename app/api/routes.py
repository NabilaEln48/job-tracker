from fastapi import APIRouter, UploadFile, File, HTTPException
from app.services.parser import parse_mbox_content as parse_mbox
from app.db.mongodb import db_client 
from bson import ObjectId
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

router = APIRouter()

# Helper to bridge the db_client to the route logic
async def get_database():
    if db_client.db is None:
        raise HTTPException(status_code=500, detail="Database not initialized")
    return db_client.db

# Schema for Manual Entry/Edits
class ApplicationUpdate(BaseModel):
    company: str
    position: str
    status: str = "applied"
    location: Optional[str] = None
    applied_date: str = Field(default_factory=lambda: datetime.now().isoformat())
    notes: Optional[str] = None

# 1. Automatic: MBOX Upload
@router.post("/upload")
async def upload_mbox(file: UploadFile = File(...)):
    content = await file.read()
    results = parse_mbox(content)
    
    db = await get_database()
    if results:
        await db.applications.insert_many(results)
    return {"status": "success", "count": len(results)}

# 2. Manual: Add New Application (LinkedIn/Indeed)
@router.post("/applications")
async def add_application(app: ApplicationUpdate):
    db = await get_database()
    new_app = app.dict()
    result = await db.applications.insert_one(new_app)
    return {"id": str(result.inserted_id)}

# 3. Read: Get All
@router.get("/applications")
async def get_applications():
    db = await get_database()
    cursor = db.applications.find().sort("applied_date", -1)
    apps = await cursor.to_list(length=1000)
    for app in apps:
        app["_id"] = str(app["_id"])
    return apps

# 4. Update: Edit Existing
@router.put("/applications/{app_id}")
async def update_application(app_id: str, app_data: ApplicationUpdate):
    db = await get_database()
    result = await db.applications.update_one(
        {"_id": ObjectId(app_id)},
        {"$set": app_data.dict()}
    )
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "updated"}

# 5. Delete: Remove Application
@router.delete("/applications/{app_id}")
async def delete_application(app_id: str):
    db = await get_database()
    result = await db.applications.delete_one({"_id": ObjectId(app_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Not found")
    return {"status": "deleted"}

# 6. Analytics: Stats for the top cards
@router.get("/analytics")
async def get_analytics():
    db = await get_database()
    total = await db.applications.count_documents({})
    interviews = await db.applications.count_documents({"status": {"$regex": "interview", "$options": "i"}})
    rejected = await db.applications.count_documents({"status": {"$regex": "rejected", "$options": "i"}})
    pending = await db.applications.count_documents({"status": {"$regex": "applied", "$options": "i"}})
    
    # Rate calculations
    success_rate = (interviews / total * 100) if total > 0 else 0
    rejection_rate = (rejected / total * 100) if total > 0 else 0
    
    return {
        "totalApps": total,
        "interviews": interviews,
        "rejected": rejected,
        "pending": pending,
        "responseRate": round(success_rate, 1),
        "rejectionRate": round(rejection_rate, 1),
        "avgResponseTime": 5  # Placeholder
    }