#!/usr/bin/env python3
"""
Fix Integration Mode - Update demo mode to production mode
"""

import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

def fix_integration_mode():
    """Fix the integration mode from demo to production"""
    try:
        # Connect to MongoDB
        client = pymongo.MongoClient(MONGO_URL)
        db = client[DB_NAME]
        
        print("🔧 Fixing integration mode from 'demo' to 'production'...")
        
        # Find all integrations with mode 'demo'
        demo_integrations = list(db.integrations.find({"mode": "demo"}))
        
        print(f"Found {len(demo_integrations)} demo integrations")
        
        for integration in demo_integrations:
            print(f"\n📋 Integration Details:")
            print(f"   - User ID: {integration.get('user_id')}")
            print(f"   - Type: {integration.get('type')}")
            print(f"   - Current Mode: {integration.get('mode')}")
            print(f"   - Status: {integration.get('status')}")
            print(f"   - Email: {integration.get('email')}")
            
            # Update mode to production
            result = db.integrations.update_one(
                {"_id": integration["_id"]},
                {"$set": {"mode": "production"}}
            )
            
            if result.modified_count > 0:
                print("✅ Updated mode to 'production'")
            else:
                print("❌ Failed to update mode")
        
        # Verify the fix
        print("\n🔍 Verifying fix...")
        updated_integrations = list(db.integrations.find({"type": "zohobooks"}))
        
        for integration in updated_integrations:
            print(f"\n📋 Updated Integration:")
            print(f"   - User ID: {integration.get('user_id')}")
            print(f"   - Mode: {integration.get('mode')}")
            print(f"   - Status: {integration.get('status')}")
        
        client.close()
        return True
        
    except Exception as e:
        print(f"❌ Error fixing integration mode: {str(e)}")
        return False

if __name__ == "__main__":
    fix_integration_mode()