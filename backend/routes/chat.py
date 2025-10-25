from fastapi import APIRouter, Depends
from models import ChatMessage, ChatResponse, ChatHistory, MessageItem
from auth_utils import get_current_user
from database import init_db
from datetime import datetime
from dotenv import load_dotenv
import uuid
import os
from emergentintegrations.llm.chat import LlmChat, UserMessage
from zoho_api_helper import (
    get_user_zoho_credentials, 
    get_invoices, 
    get_customers,
    get_outstanding_receivables,
    search_invoices_by_customer
)
import json

# Load environment variables
load_dotenv()

router = APIRouter(prefix="/api/chat", tags=["Chat"])

async def get_zoho_context(user_id: str) -> str:
    """Get Zoho Books integration context for the user"""
    db = init_db()
    
    integration = await db.integrations.find_one({
        "user_id": user_id,
        "type": "zohobooks",
        "status": "active"
    })
    
    if integration and integration.get("mode") == "production":
        # User has REAL Zoho Books connected
        return f"User has Zoho Books connected (Email: {integration.get('email', 'N/A')}). You have access to their REAL accounting data via API. You can analyze actual invoices, payments, customers, and financial reports."
    elif integration and integration.get("mode") == "demo":
        return "User has Zoho Books in DEMO mode. You do NOT have access to real data."
    
    return "User does not have any accounting software connected yet."

async def fetch_zoho_data_for_query(user_id: str, query: str) -> str:
    """Fetch relevant Zoho Books data based on user's question"""
    integration = await get_user_zoho_credentials(user_id)
    
    if not integration or integration.get("mode") != "production":
        return "No real Zoho Books data available."
    
    query_lower = query.lower()
    context = []
    
    try:
        # Fetch relevant data based on query
        if any(word in query_lower for word in ['invoice', 'overdue', 'outstanding', 'unpaid']):
            invoices = await get_invoices(user_id, status="overdue")
            if invoices:
                top_overdue = sorted(invoices, key=lambda x: float(x.get('balance', 0)), reverse=True)[:5]
                context.append("Top 5 Overdue Invoices:")
                for inv in top_overdue:
                    context.append(f"- Invoice #{inv.get('invoice_number')}: {inv.get('customer_name')} - ₹{inv.get('balance')} (Due: {inv.get('due_date')})")
        
        if any(word in query_lower for word in ['customer', 'client', 'account']):
            customers = await get_customers(user_id)
            if customers:
                context.append(f"\nTotal Customers: {len(customers)}")
                context.append("Recent Customers:")
                for cust in customers[:3]:
                    context.append(f"- {cust.get('contact_name')}: Outstanding ₹{cust.get('outstanding_receivable_amount', 0)}")
        
        if any(word in query_lower for word in ['receivable', 'collection', 'summary', 'total']):
            receivables = await get_outstanding_receivables(user_id)
            if receivables:
                context.append(f"\nOutstanding Receivables Summary:")
                context.append(f"- Total Outstanding: ₹{receivables.get('total_outstanding', 0)}")
        
        return "\n".join(context) if context else "Fetched data but no specific matches found."
        
    except Exception as e:
        return f"Error fetching Zoho data: {str(e)}"

async def generate_ai_response(user_message: str, user_id: str, chat_history: list = None) -> str:
    """Generate AI response using OpenAI GPT-5 Nano with Zoho Books context"""
    
    # Get integration context
    zoho_context = await get_zoho_context(user_id)
    
    # Check if user has any Zoho Books integration (demo or production)
    db = init_db()
    integration = await db.integrations.find_one({
        "user_id": user_id,
        "type": "zohobooks",
        "status": "active"
    })
    
    is_connected = integration is not None
    is_production_mode = integration and integration.get("mode") == "production"
    
    # Fetch actual Zoho data if connected
    zoho_data_context = ""
    if is_connected:
        zoho_data_context = await fetch_zoho_data_for_query(user_id, user_message)
    
    dummy_data_instruction = ""
    if not is_connected:
        dummy_data_instruction = "IMPORTANT: The user does NOT have accounting software connected yet. When providing ANY specific numbers, amounts, statistics, or data-based insights, you MUST start your entire response with '[DUMMY DATA]' at the very beginning. This tag is mandatory for all responses involving data until they connect their accounting system."
    
    real_data_section = ""
    if is_connected and zoho_data_context:
        real_data_section = f"REAL DATA FROM ZOHO BOOKS:\n{zoho_data_context}\n\nUse this ACTUAL data to answer the user's question accurately. Reference specific invoice numbers, customer names, and amounts from the data above."
    
    # Build system prompt with context
    system_prompt = f"""You are an AI Collections Assistant for Vasool, a credit collections management platform. 

Your role is to help users with:
- Analyzing collections portfolios and outstanding debts
- Tracking payments and reconciliation
- Optimizing collection strategies
- Providing insights on recovery rates and debtor behavior
- Understanding compliance requirements (RBI guidelines)
- Managing communication with debtors

Integration Status:
{zoho_context}

{dummy_data_instruction}

{real_data_section}

When the user has Zoho Books connected, you can help them:
- Analyze invoice data and outstanding receivables
- Track payment patterns
- Identify overdue accounts
- Suggest collection strategies based on their accounting data
- Generate financial reports for collections

Be professional, empathetic, and provide actionable insights. Keep responses concise and focused on collections management."""

    try:
        # Initialize LlmChat with GPT-5 Nano
        api_key = os.environ.get('OPENAI_API_KEY')
        chat = LlmChat(
            api_key=api_key,
            session_id=user_id,  # Use user_id as session for now
            system_message=system_prompt
        ).with_model("openai", "gpt-5-nano")
        
        # Create user message
        user_msg = UserMessage(text=user_message)
        
        # Send message and get response
        response = await chat.send_message(user_msg)
        
        return response
    except Exception as e:
        print(f"GPT-5 Nano API Error: {str(e)}")
        # Fallback to basic response
        return "I'm here to help you with collections management. Could you please rephrase your question or provide more details?"

@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_msg: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    db = init_db()
    
    # Generate or use existing session_id
    session_id = chat_msg.session_id if chat_msg.session_id else str(uuid.uuid4())
    user_id = current_user["user_id"]
    
    # Get existing chat history for context
    chat_history = []
    if session_id:
        existing_session = await db.chat_sessions.find_one({
            "user_id": user_id,
            "session_id": session_id
        })
        if existing_session and "messages" in existing_session:
            chat_history = existing_session["messages"]
    
    # Create user message
    user_msg = {
        "sender": "user",
        "message": chat_msg.message,
        "timestamp": datetime.utcnow()
    }
    
    # Generate AI response using OpenAI
    ai_response_text = await generate_ai_response(chat_msg.message, user_id, chat_history)
    ai_msg = {
        "sender": "assistant",
        "message": ai_response_text,
        "timestamp": datetime.utcnow()
    }
    
    # Update or create chat session
    await db.chat_sessions.update_one(
        {"user_id": user_id, "session_id": session_id},
        {
            "$push": {"messages": {"$each": [user_msg, ai_msg]}},
            "$set": {"updated_at": datetime.utcnow()},
            "$setOnInsert": {"created_at": datetime.utcnow()}
        },
        upsert=True
    )
    
    return ChatResponse(
        response=ai_response_text,
        session_id=session_id,
        timestamp=ai_msg["timestamp"]
    )

@router.get("/history", response_model=ChatHistory)
async def get_chat_history(
    session_id: str = None,
    current_user: dict = Depends(get_current_user)
):
    db = init_db()
    user_id = current_user["user_id"]
    
    # Build query
    query = {"user_id": user_id}
    if session_id:
        query["session_id"] = session_id
    
    # Get chat session(s)
    if session_id:
        session = await db.chat_sessions.find_one(query)
        if session and "messages" in session:
            messages = [
                MessageItem(
                    id=str(i),
                    sender=msg["sender"],
                    message=msg["message"],
                    timestamp=msg["timestamp"]
                )
                for i, msg in enumerate(session["messages"])
            ]
            return ChatHistory(messages=messages)
    
    # Return empty or initial message
    return ChatHistory(messages=[
        MessageItem(
            id="1",
            sender="assistant",
            message="Hello! I'm your AI Collections Assistant. I can help you analyze your portfolio, track payments, and optimize your collection strategies. What would you like to know?",
            timestamp=datetime.utcnow()
        )
    ])