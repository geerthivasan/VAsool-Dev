from fastapi import APIRouter, HTTPException, Depends
from models import UserSignup, UserLogin, LoginResponse, UserResponse, StandardResponse
from auth_utils import hash_password, verify_password, create_access_token, get_current_user
from database import init_db
from datetime import datetime
from bson import ObjectId

router = APIRouter(prefix="/api/auth", tags=["Authentication"])

@router.post("/signup", response_model=StandardResponse)
async def signup(user_data: UserSignup):
    db = init_db()
    
    # Check if user already exists
    existing_user = await db.users.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Hash password and create user
    hashed_password = hash_password(user_data.password)
    user_dict = {
        "name": user_data.name,
        "email": user_data.email,
        "password": hashed_password,
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    
    result = await db.users.insert_one(user_dict)
    
    return StandardResponse(
        success=True,
        message="User created successfully"
    )

@router.post("/login", response_model=LoginResponse)
async def login(credentials: UserLogin):
    db = init_db()
    
    # Find user
    user = await db.users.find_one({"email": credentials.email})
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Verify password
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    # Create access token
    token_data = {
        "user_id": str(user["_id"]),
        "email": user["email"]
    }
    token = create_access_token(token_data)
    
    return LoginResponse(
        success=True,
        token=token,
        user=UserResponse(
            id=str(user["_id"]),
            name=user["name"],
            email=user["email"]
        )
    )

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: dict = Depends(get_current_user)):
    db = init_db()
    
    user = await db.users.find_one({"_id": current_user["user_id"]})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"]
    )