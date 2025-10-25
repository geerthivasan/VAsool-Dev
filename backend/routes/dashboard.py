from fastapi import APIRouter, Depends
from models import (
    DashboardAnalytics, ActivityItem, CollectionsData, InvoiceItem,
    AnalyticsData, MonthlyMetric, ReconciliationData, ReconciliationItem
)
from auth_utils import get_current_user
from datetime import datetime, timedelta
import random
from zoho_api_helper import (
    get_dashboard_summary, get_user_zoho_credentials,
    get_invoices, get_payments
)

router = APIRouter(prefix="/api/dashboard", tags=["Dashboard"])

@router.get("/analytics", response_model=DashboardAnalytics)
async def get_analytics(current_user: dict = Depends(get_current_user)):
    user_id = current_user["user_id"]
    
    # Check if user has Zoho Books connected
    integration = await get_user_zoho_credentials(user_id)
    
    if integration and integration.get("mode") == "production":
        # Fetch REAL data from Zoho Books
        try:
            zoho_data = await get_dashboard_summary(user_id)
            
            # Convert to dashboard format
            activities = []
            for idx, payment in enumerate(zoho_data.get("recent_payments", [])):
                activities.append(ActivityItem(
                    id=str(idx),
                    title=f"Payment received - {payment.get('payment_number', 'N/A')}",
                    description=payment.get('customer_name', 'Customer'),
                    timestamp=datetime.fromisoformat(payment.get('date', datetime.utcnow().isoformat())),
                    amount=float(payment.get('amount', 0))
                ))
            
            # Add overdue invoice notifications
            for idx, invoice in enumerate(zoho_data.get("top_overdue_invoices", [])[:3]):
                activities.append(ActivityItem(
                    id=f"overdue_{idx}",
                    title=f"Overdue Invoice - {invoice.get('invoice_number', 'N/A')}",
                    description=f"{invoice.get('customer_name', 'Customer')} - {invoice.get('due_date', 'N/A')}",
                    timestamp=datetime.fromisoformat(invoice.get('due_date', datetime.utcnow().isoformat())),
                    amount=float(invoice.get('balance', 0))
                ))
            
            # Calculate recovery rate
            total_invoices = zoho_data.get("total_invoices", 1)
            overdue_invoices = zoho_data.get("overdue_invoices", 0)
            recovery_rate = ((total_invoices - overdue_invoices) / total_invoices * 100) if total_invoices > 0 else 0
            
            return DashboardAnalytics(
                total_outstanding=zoho_data.get("total_outstanding", 0),
                recovery_rate=round(recovery_rate, 1),
                active_accounts=total_invoices,
                recent_activity=activities[:10]
            )
            
        except Exception as e:
            print(f"Error fetching Zoho data: {str(e)}")
            # Fall back to mock data on error
            pass
    
    # Mock dashboard analytics data (used when Zoho not connected or in demo mode)
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