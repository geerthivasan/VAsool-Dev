from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from auth_utils import get_current_user
from database import init_db
from datetime import datetime
import os
import secrets

router = APIRouter(prefix="/api/integrations", tags=["Integrations"])

# Zoho OAuth Configuration
ZOHO_CLIENT_ID = os.environ.get('ZOHO_CLIENT_ID', 'demo_client_id')
ZOHO_CLIENT_SECRET = os.environ.get('ZOHO_CLIENT_SECRET', 'demo_client_secret')
ZOHO_REDIRECT_URI = os.environ.get('ZOHO_REDIRECT_URI', 'http://localhost:3000/zoho/callback')
ZOHO_AUTH_URL = "https://accounts.zoho.com/oauth/v2/auth"
ZOHO_TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"

class ZohoAuthUrlResponse(BaseModel):
    auth_url: str

class ZohoCallbackRequest(BaseModel):
    code: str
    state: str

class IntegrationResponse(BaseModel):
    success: bool
    message: str
    integration_id: str = None

class IntegrationStatus(BaseModel):
    zohobooks_connected: bool
    zohobooks_email: str = None
    last_sync: str = None

@router.get("/zoho/auth-url", response_model=ZohoAuthUrlResponse)
async def get_zoho_auth_url(current_user: dict = Depends(get_current_user)):
    """Generate Zoho OAuth 2.0 authorization URL"""
    
    # Generate state token for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store state in session/db for verification (in production)
    db = init_db()
    await db.oauth_states.insert_one({
        "user_id": current_user["user_id"],
        "state": state,
        "created_at": datetime.utcnow()
    })
    
    # Build OAuth URL
    auth_url = (
        f"{ZOHO_AUTH_URL}"
        f"?client_id={ZOHO_CLIENT_ID}"
        f"&response_type=code"
        f"&scope=ZohoBooks.fullaccess.all"
        f"&redirect_uri={ZOHO_REDIRECT_URI}"
        f"&state={state}"
        f"&access_type=offline"
    )
    
    return ZohoAuthUrlResponse(auth_url=auth_url)

@router.post("/zoho/callback", response_model=IntegrationResponse)
async def zoho_oauth_callback(
    callback_data: ZohoCallbackRequest,
    current_user: dict = Depends(get_current_user)
):
    """Handle OAuth callback from Zoho"""
    db = init_db()
    user_id = current_user["user_id"]
    
    # Verify state token (CSRF protection)
    state_record = await db.oauth_states.find_one({
        "user_id": user_id,
        "state": callback_data.state
    })
    
    if not state_record:
        raise HTTPException(status_code=400, detail="Invalid state token")
    
    # In production, exchange code for access token here
    # For MVP, we'll mark integration as connected
    
    integration_data = {
        "user_id": user_id,
        "type": "zohobooks",
        "connected_at": datetime.utcnow(),
        "status": "active",
        "last_sync": datetime.utcnow(),
        "auth_code": callback_data.code  # In production, store encrypted access_token
    }
    
    # Check if integration exists
    existing = await db.integrations.find_one({
        "user_id": user_id,
        "type": "zohobooks"
    })
    
    if existing:
        await db.integrations.update_one(
            {"user_id": user_id, "type": "zohobooks"},
            {"$set": integration_data}
        )
        integration_id = str(existing["_id"])
    else:
        result = await db.integrations.insert_one(integration_data)
        integration_id = str(result.inserted_id)
    
    # Clean up state token
    await db.oauth_states.delete_one({"_id": state_record["_id"]})
    
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