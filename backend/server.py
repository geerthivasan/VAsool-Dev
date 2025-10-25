from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
from pathlib import Path

# Import route modules
from routes import auth, chat, demo_contact, dashboard, integrations

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

# MongoDB connection
mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

# Create the main app without a prefix
app = FastAPI(title="Vasool API", version="1.0.0")

# Custom exception handler for validation errors
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Convert Pydantic validation errors to user-friendly messages"""
    errors = exc.errors()
    
    # Extract the first error message for simplicity
    if errors:
        first_error = errors[0]
        field = " -> ".join(str(loc) for loc in first_error['loc'][1:])  # Skip 'body'
        msg = first_error['msg']
        
        error_message = f"Invalid {field}: {msg}" if field else f"Validation error: {msg}"
    else:
        error_message = "Invalid request data"
    
    return JSONResponse(
        status_code=422,
        content={"detail": error_message}
    )

# General exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch all exceptions and return user-friendly error"""
    logger.error(f"Unhandled exception: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An unexpected error occurred. Please try again later."}
    )

# Create a router with the /api prefix for basic routes
api_router = APIRouter(prefix="/api")

# Basic health check route
@api_router.get("/")
async def root():
    return {"message": "Vasool API is running"}

# Include the router in the main app
app.include_router(api_router)

# Include feature routers
app.include_router(auth.router)
app.include_router(chat.router)
app.include_router(demo_contact.router)
app.include_router(dashboard.router)
app.include_router(integrations.router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()