from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorClient
from models import ChatMessage, ChatResponse, ChatHistory, MessageItem
from auth_utils import get_current_user
import os
from datetime import datetime
import uuid

router = APIRouter(prefix="/api/chat", tags=["Chat"])

# Get database
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

def generate_ai_response(user_message: str) -> str:
    """Generate mock AI response based on user message"""
    lowerMessage = user_message.lower()
    if 'portfolio' in lowerMessage or 'collection' in lowerMessage:
        return "I can help you analyze your collections portfolio. Based on current data, you have several accounts requiring attention. Would you like me to prioritize them by recovery probability or outstanding amount?"
    elif 'payment' in lowerMessage or 'track' in lowerMessage:
        return "I'm tracking all payment activities in real-time. Let me pull up the latest payment reconciliation report for you. Any specific time period you'd like to review?"
    elif 'strategy' in lowerMessage or 'optimize' in lowerMessage:
        return "I can help optimize your collection strategies. Our AI agents have identified several accounts that would benefit from personalized outreach. Shall I draft some communication templates?"
    else:
        return "I understand you're asking about collections management. I can help with portfolio analysis, payment tracking, strategy optimization, and compliance monitoring. What specific area would you like to explore?"

@router.post("/message", response_model=ChatResponse)
async def send_message(
    chat_msg: ChatMessage,
    current_user: dict = Depends(get_current_user)
):
    # Generate or use existing session_id
    session_id = chat_msg.session_id if chat_msg.session_id else str(uuid.uuid4())
    user_id = current_user["user_id"]
    
    # Create user message
    user_msg = {
        "sender": "user",
        "message": chat_msg.message,
        "timestamp": datetime.utcnow()
    }
    
    # Generate AI response
    ai_response_text = generate_ai_response(chat_msg.message)
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