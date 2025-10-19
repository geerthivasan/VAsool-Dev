from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# User Models
class UserSignup(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

class LoginResponse(BaseModel):
    success: bool
    token: str
    user: UserResponse

# Chat Models
class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str
    timestamp: datetime

class MessageItem(BaseModel):
    id: str
    sender: str
    message: str
    timestamp: datetime

class ChatHistory(BaseModel):
    messages: List[MessageItem]

# Demo & Contact Models
class DemoRequest(BaseModel):
    name: str
    email: EmailStr
    company: str
    phone: str

class ContactRequest(BaseModel):
    name: str
    email: EmailStr
    message: str

class StandardResponse(BaseModel):
    success: bool
    message: str

# Dashboard Models
class ActivityItem(BaseModel):
    id: str
    title: str
    description: str
    timestamp: datetime
    amount: Optional[float] = None

class DashboardAnalytics(BaseModel):
    total_outstanding: float
    recovery_rate: float
    active_accounts: int
    recent_activity: List[ActivityItem]