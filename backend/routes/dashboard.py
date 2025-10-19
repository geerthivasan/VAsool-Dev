from fastapi import APIRouter, Depends
from models import DashboardAnalytics, ActivityItem
from auth_utils import get_current_user
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/analytics", response_model=DashboardAnalytics)
async def get_analytics(current_user: dict = Depends(get_current_user)):
    # Mock dashboard analytics data
    # In production, this would fetch real data from database
    
    activities = [
        ActivityItem(
            id="1",
            title="Payment received - INV-2024-001",
            description="2 hours ago",
            timestamp=datetime.utcnow() - timedelta(hours=2),
            amount=25000
        ),
        ActivityItem(
            id="2",
            title="New collection strategy activated",
            description="5 hours ago",
            timestamp=datetime.utcnow() - timedelta(hours=5),
            amount=None
        ),
        ActivityItem(
            id="3",
            title="Communication sent - Account XYZ",
            description="1 day ago",
            timestamp=datetime.utcnow() - timedelta(days=1),
            amount=None
        ),
        ActivityItem(
            id="4",
            title="Payment received - INV-2024-002",
            description="2 days ago",
            timestamp=datetime.utcnow() - timedelta(days=2),
            amount=15000
        ),
    ]
    
    return DashboardAnalytics(
        total_outstanding=4520000,  # 45.2L
        recovery_rate=68.0,
        active_accounts=124,
        recent_activity=activities
    )