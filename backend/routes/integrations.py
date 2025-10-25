from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel, EmailStr
from typing import Optional
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

class UserOAuthSetup(BaseModel):
    client_id: str
    client_secret: str
    organization_id: Optional[str] = None

@router.post("/zoho/user-oauth-setup", response_model=ZohoAuthUrlResponse)
async def user_oauth_setup(
    oauth_data: UserOAuthSetup,
    current_user: dict = Depends(get_current_user)
):
    """Store user's OAuth credentials and generate auth URL"""
    db = init_db()
    user_id = current_user["user_id"]
    
    # Generate state token for CSRF protection
    state = secrets.token_urlsafe(32)
    
    # Store OAuth credentials and state for this user
    await db.user_oauth_credentials.insert_one({
        "user_id": user_id,
        "client_id": oauth_data.client_id,
        "client_secret": oauth_data.client_secret,  # Should be encrypted in production
        "organization_id": oauth_data.organization_id,
        "state": state,
        "created_at": datetime.utcnow()
    })
    
    # Build redirect URI for this user
    redirect_uri = f"{os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:3000')}/zoho/callback"
    
    # Build OAuth URL using user's credentials
    auth_url = (
        f"{ZOHO_AUTH_URL}"
        f"?scope={ZOHO_SCOPE}"
        f"&client_id={oauth_data.client_id}"
        f"&response_type=code"
        f"&redirect_uri={redirect_uri}"
        f"&state={state}"
        f"&access_type=offline"
        f"&prompt=consent"
    )
    
    return ZohoAuthUrlResponse(auth_url=auth_url, state=state)

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

@router.get("/zoho/config-status")
async def get_zoho_config_status():
    """Check if Zoho OAuth is properly configured (for admin/debugging)"""
    is_configured = not (
        ZOHO_CLIENT_ID.startswith('1000.YOUR') or 
        ZOHO_CLIENT_SECRET == 'your_client_secret'
    )
    
    return {
        "configured": is_configured,
        "client_id_set": bool(ZOHO_CLIENT_ID and not ZOHO_CLIENT_ID.startswith('1000.YOUR')),
        "client_secret_set": bool(ZOHO_CLIENT_SECRET and ZOHO_CLIENT_SECRET != 'your_client_secret'),
        "redirect_uri": ZOHO_REDIRECT_URI,
        "message": "OAuth configured - users can connect with Zoho login" if is_configured 
                   else "OAuth not configured - users will see Demo Mode option. Add ZOHO_CLIENT_ID and ZOHO_CLIENT_SECRET to enable real OAuth."
    }

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
    
    # Get user's OAuth credentials and verify state
    user_oauth = await db.user_oauth_credentials.find_one({
        "user_id": user_id,
        "state": callback_data.state
    })
    
    if not user_oauth:
        raise HTTPException(status_code=400, detail="Invalid state token or OAuth setup not found")
    
    # Use user's credentials for token exchange
    client_id = user_oauth["client_id"]
    client_secret = user_oauth["client_secret"]
    redirect_uri = f"{os.environ.get('REACT_APP_BACKEND_URL', 'http://localhost:3000')}/zoho/callback"
    
    # Exchange authorization code for access token
    try:
        async with httpx.AsyncClient() as http_client:
            token_response = await http_client.post(
                ZOHO_TOKEN_URL,
                data={
                    "code": callback_data.code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "redirect_uri": redirect_uri,
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
                "email": current_user.get("email"),
                "organization_id": user_oauth.get("organization_id"),
                "connected_at": datetime.utcnow(),
                "status": "active",
                "last_sync": datetime.utcnow(),
                "access_token": token_data.get("access_token"),  # Should be encrypted in production
                "refresh_token": token_data.get("refresh_token"),  # Should be encrypted in production
                "token_expires_in": token_data.get("expires_in"),
                "client_id": client_id,
                "client_secret": client_secret,  # Should be encrypted in production
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
            
            # Clean up OAuth credentials document
            await db.user_oauth_credentials.delete_one({"_id": user_oauth["_id"]})
            
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