#!/usr/bin/env python3
"""
Debug Zoho API Calls - Check what happens when dashboard tries to fetch real data
"""

import requests
import json
import sys
from datetime import datetime
import pymongo
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/app/backend/.env')

# Configuration
BASE_URL = "https://fintech-collector.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"
MONGO_URL = os.environ.get('MONGO_URL', 'mongodb://localhost:27017')
DB_NAME = os.environ.get('DB_NAME', 'test_database')

# Test user credentials
TEST_USER = {
    "name": "Debug Test User",
    "email": "debugtest@test.com", 
    "password": "testpass123"
}

class ZohoAPIDebugger:
    def __init__(self):
        self.auth_token = None
        self.user_id = None
        self.mongo_client = None
        self.db = None
        
    def connect_to_mongodb(self):
        """Connect to MongoDB"""
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_URL)
            self.db = self.mongo_client[DB_NAME]
            print("✅ Connected to MongoDB successfully")
            return True
        except Exception as e:
            print(f"❌ Failed to connect to MongoDB: {str(e)}")
            return False
    
    def make_request(self, method, endpoint, data=None, headers=None):
        """Make HTTP request with error handling"""
        url = f"{API_BASE}{endpoint}"
        
        try:
            if headers is None:
                headers = {"Content-Type": "application/json"}
                
            if method.upper() == "GET":
                response = requests.get(url, headers=headers, timeout=30)
            elif method.upper() == "POST":
                response = requests.post(url, json=data, headers=headers, timeout=30)
            else:
                raise ValueError(f"Unsupported method: {method}")
                
            return response
            
        except requests.exceptions.RequestException as e:
            print(f"Request failed for {endpoint}: {str(e)}")
            return None
    
    def authenticate_user(self):
        """Authenticate user and get token"""
        print("🔐 Authenticating user...")
        
        # Try to register user (might already exist)
        signup_response = self.make_request("POST", "/auth/signup", TEST_USER)
        
        # Login to get token
        login_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        login_response = self.make_request("POST", "/auth/login", login_data)
        
        if login_response and login_response.status_code == 200:
            try:
                data = login_response.json()
                if data.get("success") and data.get("token"):
                    self.auth_token = data["token"]
                    user_data = data.get("user", {})
                    self.user_id = user_data.get("id")
                    print(f"✅ Authentication successful. User ID: {self.user_id}")
                    return True
                else:
                    print("❌ Login response missing success or token")
            except json.JSONDecodeError:
                print("❌ Invalid JSON response from login")
        else:
            print(f"❌ Login failed with status {login_response.status_code if login_response else 'None'}")
            
        return False
    
    def create_demo_integration(self):
        """Create demo integration"""
        print("🔧 Creating demo integration...")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("POST", "/integrations/zoho/demo-connect", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if data.get('success'):
                    print("✅ Demo integration created successfully")
                    return True
                else:
                    print(f"❌ Demo integration failed: {data.get('message', 'Unknown error')}")
            except json.JSONDecodeError:
                print("❌ Invalid JSON response from demo connect")
        else:
            print(f"❌ Demo connect failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def check_integration_in_db(self):
        """Check what's actually stored in the integration"""
        print("\n🔍 Checking integration in database...")
        
        if self.db is None or not self.user_id:
            print("❌ No database connection or user ID")
            return None
            
        try:
            integration = self.db.integrations.find_one({
                "user_id": self.user_id,
                "type": "zohobooks"
            })
            
            if integration:
                print("✅ Found integration:")
                print(f"   - Mode: {integration.get('mode', 'NOT SET')}")
                print(f"   - Status: {integration.get('status', 'NOT SET')}")
                print(f"   - Access Token: {'YES' if integration.get('access_token') else 'NO'}")
                print(f"   - Client ID: {'YES' if integration.get('client_id') else 'NO'}")
                print(f"   - Organization ID: {integration.get('organization_id', 'NOT SET')}")
                return integration
            else:
                print("❌ No integration found")
                return None
                
        except Exception as e:
            print(f"❌ Error checking integration: {str(e)}")
            return None
    
    def test_dashboard_with_debug(self):
        """Test dashboard endpoint and see what happens"""
        print("\n🧪 Testing dashboard collections with debug info...")
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/collections", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                
                print("📊 Dashboard Collections Response:")
                print(f"   - Total Unpaid: {data.get('total_unpaid', 0)}")
                print(f"   - Total Overdue: {data.get('total_overdue', 0)}")
                print(f"   - Unpaid Count: {len(data.get('unpaid_invoices', []))}")
                print(f"   - Overdue Count: {len(data.get('overdue_invoices', []))}")
                
                # Check if this is mock data
                if data.get('total_unpaid') == 125000:
                    print("❌ CONFIRMED: Still returning mock data")
                    print("   This means the dashboard is NOT using production mode logic")
                else:
                    print("✅ Returning real/empty data (not mock)")
                
                return True
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
        else:
            print(f"❌ Dashboard request failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def fix_integration_mode_to_production(self):
        """Fix integration mode to production"""
        print("\n🔧 Fixing integration mode to production...")
        
        if not self.db or not self.user_id:
            print("❌ No database connection or user ID")
            return False
            
        try:
            result = self.db.integrations.update_one(
                {"user_id": self.user_id, "type": "zohobooks"},
                {"$set": {"mode": "production"}}
            )
            
            if result.modified_count > 0:
                print("✅ Updated integration mode to production")
                return True
            else:
                print("❌ Failed to update integration mode")
                return False
                
        except Exception as e:
            print(f"❌ Error updating integration: {str(e)}")
            return False
    
    def run_debug_session(self):
        """Run complete debug session"""
        print("🐛 ZOHO API DEBUG SESSION")
        print("Investigating why dashboard shows mock data despite production mode")
        print("="*80)
        
        # Connect to MongoDB
        if not self.connect_to_mongodb():
            return False
        
        # Authenticate user
        if not self.authenticate_user():
            return False
        
        # Create demo integration
        if not self.create_demo_integration():
            return False
        
        # Check integration in database
        integration = self.check_integration_in_db()
        
        # Test dashboard before fix
        print("\n📊 TESTING DASHBOARD BEFORE FIX:")
        self.test_dashboard_with_debug()
        
        # Fix integration mode
        if integration and integration.get("mode") != "production":
            self.fix_integration_mode_to_production()
            
            # Test dashboard after fix
            print("\n📊 TESTING DASHBOARD AFTER FIX:")
            self.test_dashboard_with_debug()
        
        # Check backend logs for any Zoho API errors
        print("\n📋 Checking backend logs for Zoho API errors...")
        try:
            import subprocess
            result = subprocess.run(
                ["tail", "-n", "20", "/var/log/supervisor/backend.err.log"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logs = result.stdout
                if "zoho" in logs.lower() or "error fetching" in logs.lower():
                    print("⚠️  Found Zoho-related errors in logs:")
                    print(logs)
                else:
                    print("✅ No Zoho API errors in recent logs")
            else:
                print("❌ Could not read backend logs")
                
        except Exception as e:
            print(f"❌ Error reading logs: {str(e)}")
        
        # Final analysis
        print("\n" + "="*80)
        print("🎯 DEBUG ANALYSIS")
        print("="*80)
        
        if integration:
            mode = integration.get("mode")
            has_token = bool(integration.get("access_token"))
            
            print(f"Integration Mode: {mode}")
            print(f"Has Access Token: {has_token}")
            
            if mode == "production" and not has_token:
                print("\n❌ ROOT CAUSE IDENTIFIED:")
                print("   - Integration is in 'production' mode")
                print("   - But no access_token is available")
                print("   - Dashboard tries to fetch real data, fails, falls back to mock data")
                print("\n📋 SOLUTION:")
                print("   - For demo purposes: Dashboard should check for access_token")
                print("   - If no token but mode=production, should return empty data (not mock)")
                print("   - For real usage: User needs to complete OAuth flow to get access_token")
            elif mode != "production":
                print(f"\n❌ Integration mode is '{mode}', should be 'production'")
            else:
                print("\n✅ Integration appears correctly configured")
        
        # Close MongoDB connection
        if self.mongo_client:
            self.mongo_client.close()
            
        return True

if __name__ == "__main__":
    debugger = ZohoAPIDebugger()
    success = debugger.run_debug_session()
    sys.exit(0 if success else 1)