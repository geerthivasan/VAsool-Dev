from motor.motor_asyncio import AsyncIOMotorClient
import os

# Get MongoDB connection
def get_database():
    mongo_url = os.environ.get('MONGO_URL')
    if not mongo_url:
        raise ValueError(\"MONGO_URL environment variable not set\")
    
    client = AsyncIOMotorClient(mongo_url)
    db_name = os.environ.get('DB_NAME', 'vasool_db')
    return client[db_name]

# Initialize database
db = None

def init_db():
    global db
    if db is None:
        db = get_database()
    return db
