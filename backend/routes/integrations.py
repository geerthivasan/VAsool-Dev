from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from auth_utils import get_current_user
from database import init_db
from datetime import datetime
import os
import secrets
import httpx

router = APIRouter(prefix="/api/integrations", tags=["Integrations"])

# Zoho OAuth Configuration
ZOHO_CLIENT_ID = os.environ.get('ZOHO_CLIENT_ID', '1000.YOUR_CLIENT_ID')
ZOHO_CLIENT_SECRET = os.environ.get('ZOHO_CLIENT_SECRET', 'your_client_secret')
ZOHO_REDIRECT_URI = os.environ.get('ZOHO_REDIRECT_URI', f'{os.environ.get("REACT_APP_BACKEND_URL", "http://localhost:3000")}/zoho/callback')
ZOHO_AUTH_URL = "https://accounts.zoho.com/oauth/v2/auth"
ZOHO_TOKEN_URL = "https://accounts.zoho.com/oauth/v2/token"
ZOHO_SCOPE = "ZohoBooks.fullaccess.all"

class ZohoAuthUrlResponse(BaseModel):
    auth_url: str
    state: str

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

@router.post("/zoho/demo-connect", response_model=IntegrationResponse)
async def demo_connect_zoho(current_user: dict = Depends(get_current_user)):
    """Demo mode connection for testing without real OAuth credentials"""
    db = init_db()
    user_id = current_user["user_id"]
    
    integration_data = {
        "user_id": user_id,
        "type": "zohobooks",
        "email": "demo@zohobooks.com",
        "connected_at": datetime.utcnow(),
        "status": "active",
        "last_sync": datetime.utcnow(),
        "mode": "demo"
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
    
    return IntegrationResponse(
        success=True,
        message="Zoho Books connected in demo mode",
        integration_id=integration_id
    )

@router.get("/zoho/auth-url", response_model=ZohoAuthUrlResponse)
async def get_zoho_auth_url(current_user: dict = Depends(get_current_user)):
    """Generate Zoho OAuth 2.0 authorization URL following official Zoho Books API documentation"""
    
    # Check if real OAuth credentials are configured
    if ZOHO_CLIENT_ID.startswith('1000.YOUR') or ZOHO_CLIENT_SECRET == 'your_client_secret':
        raise HTTPException(
            status_code=400, 
            detail="Zoho OAuth credentials not configured. Please set ZOHO_CLIENT_ID and ZOHO_CLIENT_SECRET in environment variables, or use Demo Mode."
        )
    
    # Generate state token for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store state in session/db for verification
    db = init_db()
    await db.oauth_states.insert_one({
        "user_id": current_user["user_id"],
        "state": state,
        "created_at": datetime.utcnow()
    })
    
    # Build OAuth URL exactly as per Zoho Books API documentation
    auth_url = (
        f"{ZOHO_AUTH_URL}"
        f"?scope={ZOHO_SCOPE}"
        f"&client_id={ZOHO_CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={ZOHO_REDIRECT_URI}"
        f"&state={state}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    
    return ZohoAuthUrlResponse(auth_url=auth_url, state=state)

@router.post("/zoho/callback", response_model=IntegrationResponse)
async def zoho_oauth_callback(
    callback_data: ZohoCallbackRequest,
    current_user: dict = Depends(get_current_user)
):
    """Handle OAuth callback from Zoho and exchange code for access token"""
    db = init_db()
    user_id = current_user["user_id"]
    
    # Verify state token (CSRF protection)
    state_record = await db.oauth_states.find_one({
        "user_id": user_id,
        "state": callback_data.state
    })
    
    if not state_record:
        raise HTTPException(status_code=400, detail="Invalid state token")
    
    # Exchange authorization code for access token
    try:
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                ZOHO_TOKEN_URL,
                data={
                    "code": callback_data.code,
                    "client_id": ZOHO_CLIENT_ID,
                    "client_secret": ZOHO_CLIENT_SECRET,
                    "redirect_uri": ZOHO_REDIRECT_URI,
                    "grant_type": "authorization_code"
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            
            if token_response.status_code != 200:
                raise HTTPException(
                    status_code=400, 
                    detail=f"Failed to exchange code for token: {token_response.text}"
                )
            
            token_data = token_response.json()
            
            # Store access token and refresh token securely
            integration_data = {
                "user_id": user_id,
                "type": "zohobooks",
                "connected_at": datetime.utcnow(),
                "status": "active",
                "last_sync": datetime.utcnow(),
                "access_token": token_data.get("access_token"),  # Should be encrypted in production
                "refresh_token": token_data.get("refresh_token"),  # Should be encrypted in production
                "token_expires_in": token_data.get("expires_in"),
                "mode": "production"
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
            
    except httpx.RequestError as e:
        raise HTTPException(status_code=500, detail=f"Network error: {str(e)}")

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