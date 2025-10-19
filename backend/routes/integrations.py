from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, EmailStr
from auth_utils import get_current_user
from database import init_db
from datetime import datetime
import os

router = APIRouter(prefix="/api/integrations", tags=["Integrations"])

class ZohoCredentials(BaseModel):
    email: EmailStr
    password: str

class IntegrationResponse(BaseModel):
    success: bool
    message: str
    integration_id: str = None

class IntegrationStatus(BaseModel):
    zohobooks_connected: bool
    zohobooks_email: str = None
    last_sync: str = None

@router.post("/zoho/connect", response_model=IntegrationResponse)
async def connect_zoho(
    credentials: ZohoCredentials,
    current_user: dict = Depends(get_current_user)
):
    db = init_db()
    user_id = current_user["user_id"]
    
    # In production, this would:
    # 1. Validate credentials with Zoho OAuth 2.0
    # 2. Store encrypted access tokens
    # 3. Set up webhook for data sync
    
    # For MVP, we'll store the connection status
    integration_data = {
        "user_id": user_id,
        "type": "zohobooks",
        "email": credentials.email,
        "connected_at": datetime.utcnow(),
        "status": "active",
        "last_sync": datetime.utcnow()
    }
    
    # Check if integration already exists
    existing = await db.integrations.find_one({
        "user_id": user_id,
        "type": "zohobooks"
    })
    
    if existing:
        # Update existing integration
        await db.integrations.update_one(
            {"user_id": user_id, "type": "zohobooks"},
            {"$set": integration_data}
        )
        integration_id = str(existing["_id"])
    else:
        # Create new integration
        result = await db.integrations.insert_one(integration_data)
        integration_id = str(result.inserted_id)
    
    return IntegrationResponse(
        success=True,
        message="Zoho Books connected successfully",
        integration_id=integration_id
    )

@router.get("/status", response_model=IntegrationStatus)
async def get_integration_status(
    current_user: dict = Depends(get_current_user)
):
    db = init_db()
    user_id = current_user["user_id"]
    
    # Check for Zoho Books integration
    zoho_integration = await db.integrations.find_one({
        "user_id": user_id,
        "type": "zohobooks",
        "status": "active"
    })
    
    if zoho_integration:
        return IntegrationStatus(
            zohobooks_connected=True,
            zohobooks_email=zoho_integration.get("email"),
            last_sync=zoho_integration.get("last_sync").isoformat() if zoho_integration.get("last_sync") else None
        )
    
    return IntegrationStatus(
        zohobooks_connected=False
    )

@router.delete("/zoho/disconnect")
async def disconnect_zoho(
    current_user: dict = Depends(get_current_user)
):
    db = init_db()
    user_id = current_user["user_id"]
    
    # Deactivate integration
    result = await db.integrations.update_one(
        {"user_id": user_id, "type": "zohobooks"},
        {"$set": {"status": "inactive", "disconnected_at": datetime.utcnow()}}
    )
    
    return {"success": True, "message": "Zoho Books disconnected successfully"}