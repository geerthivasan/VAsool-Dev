from fastapi import APIRouter
from models import DemoRequest, ContactRequest, StandardResponse
from database import init_db
from datetime import datetime

router = APIRouter(prefix="/api", tags=["Demo & Contact"])

@router.post("/demo/schedule", response_model=StandardResponse)
async def schedule_demo(demo_req: DemoRequest):
    db = init_db()
    
    # Save demo request
    demo_dict = {
        "name": demo_req.name,
        "email": demo_req.email,
        "company": demo_req.company,
        "phone": demo_req.phone,
        "status": "pending",
        "created_at": datetime.utcnow()
    }
    
    await db.demo_requests.insert_one(demo_dict)
    
    return StandardResponse(
        success=True,
        message="Demo request received. We'll contact you shortly!"
    )

@router.post("/contact/sales", response_model=StandardResponse)
async def contact_sales(contact_req: ContactRequest):
    db = init_db()
    
    # Save contact message
    contact_dict = {
        "name": contact_req.name,
        "email": contact_req.email,
        "message": contact_req.message,
        "status": "new",
        "created_at": datetime.utcnow()
    }
    
    await db.contact_messages.insert_one(contact_dict)
    
    return StandardResponse(
        success=True,
        message="Message sent successfully. Our sales team will reach out soon!"
    )