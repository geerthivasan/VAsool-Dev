#!/usr/bin/env python3
"""
Check current integration mode in database
"""

import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv('/app/backend/.env')

async def check_integration_mode():
    # Connect to MongoDB
    mongo_url = os.environ['MONGO_URL']
    client = AsyncIOMotorClient(mongo_url)
    db = client[os.environ['DB_NAME']]
    
    print("🔍 Checking Zoho Books Integration Status in Database")
    print("=" * 60)
    
    # Find all integrations
    integrations = await db.integrations.find({"type": "zohobooks"}).to_list(None)
    
    if not integrations:
        print("❌ No Zoho Books integrations found in database")
        return
    
    print(f"Found {len(integrations)} Zoho Books integration(s):")
    print()
    
    for i, integration in enumerate(integrations, 1):
        print(f"Integration {i}:")
        print(f"  User ID: {integration.get('user_id', 'N/A')}")
        print(f"  Email: {integration.get('email', 'N/A')}")
        print(f"  Status: {integration.get('status', 'N/A')}")
        print(f"  Mode: {integration.get('mode', 'N/A')}")
        print(f"  Connected At: {integration.get('connected_at', 'N/A')}")
        print(f"  Last Sync: {integration.get('last_sync', 'N/A')}")
        print(f"  Has Access Token: {'Yes' if integration.get('access_token') else 'No'}")
        print(f"  Has Refresh Token: {'Yes' if integration.get('refresh_token') else 'No'}")
        print(f"  Organization ID: {integration.get('organization_id', 'N/A')}")
        print()
    
    # Check if any are in demo mode that should be production
    demo_integrations = [i for i in integrations if i.get('mode') == 'demo']
    production_integrations = [i for i in integrations if i.get('mode') == 'production']
    
    print("📊 Summary:")
    print(f"  Demo Mode: {len(demo_integrations)}")
    print(f"  Production Mode: {len(production_integrations)}")
    
    if demo_integrations:
        print("\n⚠️  ISSUE IDENTIFIED:")
        print("  Some integrations are in 'demo' mode instead of 'production' mode.")
        print("  This causes dashboard to show mock data instead of real Zoho data.")
        
        print("\n🔧 FIXING INTEGRATION MODES...")
        
        # Update all demo integrations to production mode
        for integration in demo_integrations:
            if integration.get('access_token'):  # Only if they have real tokens
                result = await db.integrations.update_one(
                    {"_id": integration["_id"]},
                    {"$set": {"mode": "production"}}
                )
                print(f"  ✅ Updated integration for user {integration.get('user_id')} to production mode")
            else:
                print(f"  ⚠️  Integration for user {integration.get('user_id')} has no access token - keeping in demo mode")
        
        print("\n✅ Integration modes updated!")
    else:
        print("\n✅ All integrations are properly configured")
    
    client.close()

if __name__ == "__main__":
    asyncio.run(check_integration_mode())