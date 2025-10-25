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
    


@router.get("/collections", response_model=CollectionsData)
async def get_collections(current_user: dict = Depends(get_current_user)):
    """Get collections data - unpaid and overdue invoices"""
    user_id = current_user["user_id"]
    
    # Check if user has Zoho Books connected
    integration = await get_user_zoho_credentials(user_id)
    
    if integration and integration.get("mode") == "production":
        try:
            # Fetch real data from Zoho
            unpaid = await get_invoices(user_id, status="unpaid") or []
            overdue = await get_invoices(user_id, status="overdue") or []
            
            # Convert to our format
            unpaid_items = []
            for inv in unpaid:
                days_overdue = None
                due_date = inv.get('due_date', '')
                if due_date:
                    try:
                        due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                        days_overdue = (datetime.utcnow() - due).days if due < datetime.utcnow() else 0
                    except:
                        pass
                
                unpaid_items.append(InvoiceItem(
                    id=inv.get('invoice_id', ''),
                    invoice_number=inv.get('invoice_number', 'N/A'),
                    customer_name=inv.get('customer_name', 'Unknown'),
                    amount=float(inv.get('total', 0)),
                    balance=float(inv.get('balance', 0)),
                    due_date=due_date,
                    status=inv.get('status', 'unpaid'),
                    days_overdue=days_overdue
                ))
            
            overdue_items = []
            for inv in overdue:
                days_overdue = None
                due_date = inv.get('due_date', '')
                if due_date:
                    try:
                        due = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
                        days_overdue = (datetime.utcnow() - due).days
                    except:
                        pass
                
                overdue_items.append(InvoiceItem(
                    id=inv.get('invoice_id', ''),
                    invoice_number=inv.get('invoice_number', 'N/A'),
                    customer_name=inv.get('customer_name', 'Unknown'),
                    amount=float(inv.get('total', 0)),
                    balance=float(inv.get('balance', 0)),
                    due_date=due_date,
                    status='overdue',
                    days_overdue=days_overdue
                ))
            
            total_unpaid = sum(item.balance for item in unpaid_items)
            total_overdue = sum(item.balance for item in overdue_items)
            
            return CollectionsData(
                unpaid_invoices=unpaid_items,
                overdue_invoices=overdue_items,
                total_unpaid=total_unpaid,
                total_overdue=total_overdue
            )
        except Exception as e:
            print(f"Error fetching Zoho collections: {str(e)}")
            # Fall back to mock data
            pass
    
    # Mock data
    mock_unpaid = [
        InvoiceItem(
            id="inv1",
            invoice_number="INV-2024-001",
            customer_name="ABC Corp",
            amount=50000,
            balance=50000,
            due_date=(datetime.utcnow() + timedelta(days=10)).strftime("%Y-%m-%d"),
            status="unpaid",
            days_overdue=None
        ),
        InvoiceItem(
            id="inv2",
            invoice_number="INV-2024-002",
            customer_name="XYZ Ltd",
            amount=75000,
            balance=75000,
            due_date=(datetime.utcnow() + timedelta(days=5)).strftime("%Y-%m-%d"),
            status="unpaid",
            days_overdue=None
        )
    ]
    
    mock_overdue = [
        InvoiceItem(
            id="inv3",
            invoice_number="INV-2024-003",
            customer_name="DEF Industries",
            amount=120000,
            balance=120000,
            due_date=(datetime.utcnow() - timedelta(days=15)).strftime("%Y-%m-%d"),
            status="overdue",
            days_overdue=15
        ),
        InvoiceItem(
            id="inv4",
            invoice_number="INV-2024-004",
            customer_name="GHI Enterprises",
            amount=90000,
            balance=90000,
            due_date=(datetime.utcnow() - timedelta(days=30)).strftime("%Y-%m-%d"),
            status="overdue",
            days_overdue=30
        )
    ]
    
    return CollectionsData(
        unpaid_invoices=mock_unpaid,
        overdue_invoices=mock_overdue,
        total_unpaid=125000,
        total_overdue=210000
    )


@router.get("/analytics", response_model=AnalyticsData)
async def get_analytics_data(current_user: dict = Depends(get_current_user)):
    """Get analytics data - trends and metrics"""
    user_id = current_user["user_id"]
    
    # Check if user has Zoho Books connected
    integration = await get_user_zoho_credentials(user_id)
    
    if integration and integration.get("mode") == "production":
        try:
            # Fetch real data from Zoho
            payments = await get_payments(user_id) or []
            invoices = await get_invoices(user_id) or []
            
            # Calculate monthly trends (last 6 months)
            monthly_trends = []
            for i in range(6):
                month_date = datetime.utcnow() - timedelta(days=30*i)
                month_str = month_date.strftime("%B %Y")
                
                # Filter payments and invoices for this month
                month_payments = [p for p in payments if p.get('date', '').startswith(month_date.strftime("%Y-%m"))]
                month_invoices = [inv for inv in invoices if inv.get('date', '').startswith(month_date.strftime("%Y-%m"))]
                
                collected = sum(float(p.get('amount', 0)) for p in month_payments)
                outstanding = sum(float(inv.get('balance', 0)) for inv in month_invoices)
                
                monthly_trends.append(MonthlyMetric(
                    month=month_str,
                    collected=collected,
                    outstanding=outstanding
                ))
            
            # Calculate overall metrics
            total_collected = sum(float(p.get('amount', 0)) for p in payments)
            total_outstanding = sum(float(inv.get('balance', 0)) for inv in invoices)
            
            # Collection efficiency (paid / total)
            total_invoice_amount = sum(float(inv.get('total', 0)) for inv in invoices)
            efficiency = (total_collected / total_invoice_amount * 100) if total_invoice_amount > 0 else 0
            
            return AnalyticsData(
                monthly_trends=list(reversed(monthly_trends)),
                total_collected=total_collected,
                total_outstanding=total_outstanding,
                collection_efficiency=round(efficiency, 1),
                average_collection_time=25  # Placeholder, would need more complex calculation
            )
        except Exception as e:
            print(f"Error fetching Zoho analytics: {str(e)}")
            # Fall back to mock data
            pass
    
    # Mock data
    mock_trends = [
        MonthlyMetric(month="May 2024", collected=850000, outstanding=520000),
        MonthlyMetric(month="June 2024", collected=920000, outstanding=480000),
        MonthlyMetric(month="July 2024", collected=1050000, outstanding=450000),
        MonthlyMetric(month="August 2024", collected=980000, outstanding=420000),
        MonthlyMetric(month="September 2024", collected=1120000, outstanding=400000),
        MonthlyMetric(month="October 2024", collected=1200000, outstanding=380000),
    ]
    
    return AnalyticsData(
        monthly_trends=mock_trends,
        total_collected=6120000,
        total_outstanding=2650000,
        collection_efficiency=75.5,
        average_collection_time=28
    )


@router.get("/reconciliation", response_model=ReconciliationData)
async def get_reconciliation(current_user: dict = Depends(get_current_user)):
    """Get reconciliation data - matched and unmatched transactions"""
    user_id = current_user["user_id"]
    
    # Check if user has Zoho Books connected
    integration = await get_user_zoho_credentials(user_id)
    
    if integration and integration.get("mode") == "production":
        try:
            # In a real implementation, this would fetch bank statements
            # and match them with Zoho payments
            payments = await get_payments(user_id) or []
            
            matched_items = []
            unmatched_items = []
            
            # For now, mark all payments as matched
            for idx, payment in enumerate(payments):
                matched_items.append(ReconciliationItem(
                    id=payment.get('payment_id', str(idx)),
                    date=payment.get('date', ''),
                    description=f"Payment from {payment.get('customer_name', 'Unknown')}",
                    amount=float(payment.get('amount', 0)),
                    status="matched",
                    invoice_ref=payment.get('invoice_numbers', [None])[0] if payment.get('invoice_numbers') else None
                ))
            
            total_matched = sum(item.amount for item in matched_items)
            total_unmatched = 0
            
            return ReconciliationData(
                matched_items=matched_items[:20],  # Limit to 20
                unmatched_items=unmatched_items,
                total_matched=total_matched,
                total_unmatched=total_unmatched
            )
        except Exception as e:
            print(f"Error fetching Zoho reconciliation: {str(e)}")
            # Fall back to mock data
            pass
    
    # Mock data
    mock_matched = [
        ReconciliationItem(
            id="rec1",
            date=(datetime.utcnow() - timedelta(days=2)).strftime("%Y-%m-%d"),
            description="Payment from ABC Corp",
            amount=50000,
            status="matched",
            invoice_ref="INV-2024-001"
        ),
        ReconciliationItem(
            id="rec2",
            date=(datetime.utcnow() - timedelta(days=5)).strftime("%Y-%m-%d"),
            description="Payment from XYZ Ltd",
            amount=75000,
            status="matched",
            invoice_ref="INV-2024-005"
        )
    ]
    
    mock_unmatched = [
        ReconciliationItem(
            id="rec3",
            date=(datetime.utcnow() - timedelta(days=1)).strftime("%Y-%m-%d"),
            description="Bank transfer - Unknown source",
            amount=25000,
            status="unmatched",
            invoice_ref=None
        )
    ]
    
    return ReconciliationData(
        matched_items=mock_matched,
        unmatched_items=mock_unmatched,
        total_matched=125000,
        total_unmatched=25000
    )

    return DashboardAnalytics(
        total_outstanding=4520000,  # 45.2L
        recovery_rate=68.0,
        active_accounts=124,
        recent_activity=activities
    )