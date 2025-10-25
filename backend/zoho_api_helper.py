"""
Zoho Books API Helper Functions
Fetches real data from connected Zoho Books accounts
"""

import httpx
from typing import Optional, Dict, List
from database import init_db
from datetime import datetime

ZOHO_BOOKS_API_BASE = "https://books.zoho.com/api/v3"

async def get_user_zoho_credentials(user_id: str) -> Optional[Dict]:
    """Get user's Zoho Books integration details including access token"""
    db = init_db()
    integration = await db.integrations.find_one({
        "user_id": user_id,
        "type": "zohobooks",
        "status": "active"
    })
    return integration

async def refresh_zoho_token(user_id: str, refresh_token: str, client_id: str, client_secret: str) -> Optional[str]:
    """Refresh expired Zoho access token"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://accounts.zoho.com/oauth/v2/token",
                data={
                    "refresh_token": refresh_token,
                    "client_id": client_id,
                    "client_secret": client_secret,
                    "grant_type": "refresh_token"
                }
            )
            
            if response.status_code == 200:
                token_data = response.json()
                new_access_token = token_data.get("access_token")
                
                # Update token in database
                db = init_db()
                await db.integrations.update_one(
                    {"user_id": user_id, "type": "zohobooks"},
                    {"$set": {
                        "access_token": new_access_token,
                        "last_sync": datetime.utcnow()
                    }}
                )
                
                return new_access_token
    except Exception as e:
        print(f"Token refresh error: {str(e)}")
    
    return None

async def fetch_zoho_data(user_id: str, endpoint: str, params: Dict = None) -> Optional[Dict]:
    """Generic function to fetch data from Zoho Books API"""
    integration = await get_user_zoho_credentials(user_id)
    
    if not integration:
        return None
    
    access_token = integration.get("access_token")
    organization_id = integration.get("organization_id")
    
    if not access_token:
        return None
    
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }
    
    # Add organization_id to params if available
    if organization_id:
        if params is None:
            params = {}
        params["organization_id"] = organization_id
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{ZOHO_BOOKS_API_BASE}/{endpoint}",
                headers=headers,
                params=params,
                timeout=30.0
            )
            
            if response.status_code == 401:
                # Token expired, try to refresh
                refresh_token = integration.get("refresh_token")
                client_id = integration.get("client_id")
                client_secret = integration.get("client_secret")
                
                if refresh_token and client_id and client_secret:
                    new_token = await refresh_zoho_token(user_id, refresh_token, client_id, client_secret)
                    if new_token:
                        # Retry with new token
                        headers["Authorization"] = f"Zoho-oauthtoken {new_token}"
                        response = await client.get(
                            f"{ZOHO_BOOKS_API_BASE}/{endpoint}",
                            headers=headers,
                            params=params,
                            timeout=30.0
                        )
            
            if response.status_code == 200:
                return response.json()
            else:
                print(f"Zoho API Error: {response.status_code} - {response.text}")
                return None
                
    except Exception as e:
        print(f"Error fetching Zoho data: {str(e)}")
        return None

async def get_invoices(user_id: str, status: str = None) -> Optional[List[Dict]]:
    """Get invoices from Zoho Books"""
    params = {}
    if status:
        params["status"] = status  # "overdue", "unpaid", "paid", etc.
    
    data = await fetch_zoho_data(user_id, "invoices", params)
    return data.get("invoices", []) if data else []

async def get_customers(user_id: str) -> Optional[List[Dict]]:
    """Get customers from Zoho Books"""
    data = await fetch_zoho_data(user_id, "contacts", {"contact_type": "customer"})
    return data.get("contacts", []) if data else []

async def get_payments(user_id: str) -> Optional[List[Dict]]:
    """Get payments from Zoho Books"""
    data = await fetch_zoho_data(user_id, "customerpayments")
    return data.get("customerpayments", []) if data else []

async def get_outstanding_receivables(user_id: str) -> Optional[Dict]:
    """Get outstanding receivables summary"""
    data = await fetch_zoho_data(user_id, "reports/receivables")
    return data if data else None

async def get_aged_receivables(user_id: str) -> Optional[Dict]:
    """Get aged receivables report"""
    data = await fetch_zoho_data(user_id, "reports/agedreceivables")
    return data if data else None

async def get_organization_info(user_id: str) -> Optional[Dict]:
    """Get Zoho Books organization information"""
    data = await fetch_zoho_data(user_id, "organizations")
    if data and "organizations" in data and len(data["organizations"]) > 0:
        return data["organizations"][0]
    return None

async def search_invoices_by_customer(user_id: str, customer_name: str) -> Optional[List[Dict]]:
    """Search invoices by customer name"""
    params = {"search_text": customer_name}
    data = await fetch_zoho_data(user_id, "invoices", params)
    return data.get("invoices", []) if data else []

async def get_dashboard_summary(user_id: str) -> Dict:
    """Get comprehensive dashboard data from Zoho Books"""
    
    # Fetch key data in parallel would be ideal, but let's do sequential for now
    invoices = await get_invoices(user_id, status="unpaid") or []
    overdue_invoices = await get_invoices(user_id, status="overdue") or []
    recent_payments = await get_payments(user_id) or []
    
    # Calculate metrics
    total_outstanding = sum(float(inv.get("balance", 0)) for inv in invoices)
    total_overdue = sum(float(inv.get("balance", 0)) for inv in overdue_invoices)
    
    return {
        "total_outstanding": total_outstanding,
        "total_invoices": len(invoices),
        "overdue_invoices": len(overdue_invoices),
        "overdue_amount": total_overdue,
        "recent_payments": recent_payments[:5],  # Last 5 payments
        "top_overdue_invoices": sorted(
            overdue_invoices, 
            key=lambda x: float(x.get("balance", 0)), 
            reverse=True
        )[:10]
    }
