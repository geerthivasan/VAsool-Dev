from fastapi import APIRouter, Depends
from models import ChatMessage, ChatResponse, ChatHistory, MessageItem
from auth_utils import get_current_user
from database import init_db
from datetime import datetime
import uuid
import os
from openai import OpenAI

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Initialize OpenAI client
OPENAI_API_KEY = "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"
openai_client = OpenAI(api_key=OPENAI_API_KEY)

async def get_zoho_context(user_id: str) -> str:
    """Get Zoho Books integration context for the user"""
    db = init_db()
    
    integration = await db.integrations.find_one({
        "user_id": user_id,
        "type": "zohobooks",
        "status": "active"
    })
    
    if integration:
        return f"User has Zoho Books connected (Email: {integration.get('email')}). You can help them analyze their accounting data, invoices, payments, and financial reports from Zoho Books."
    
    return "User does not have any accounting system connected yet."

async def generate_ai_response(user_message: str, user_id: str, chat_history: list = None) -> str:
    """Generate AI response using OpenAI GPT with context"""
    
    # Get integration context
    zoho_context = await get_zoho_context(user_id)
    
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

When the user has Zoho Books connected, you can help them:
- Analyze invoice data and outstanding receivables
- Track payment patterns
- Identify overdue accounts
- Suggest collection strategies based on their accounting data
- Generate financial reports for collections

Be professional, empathetic, and provide actionable insights. Keep responses concise and focused on collections management."""

    # Build messages array
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add chat history if available (last 5 messages for context)
    if chat_history:
        for msg in chat_history[-5:]:
            role = "user" if msg["sender"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["message"]})
    
    # Add current user message
    messages.append({"role": "user", "content": user_message})
    
    try:
        # Call OpenAI API
        response = openai_client.chat.completions.create(
            model="gpt-4o-mini",  # Using GPT-4o-mini which is more cost-effective
            messages=messages,
            max_tokens=500,
            temperature=0.7
        )
        
        return response.choices[0].message.content
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
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