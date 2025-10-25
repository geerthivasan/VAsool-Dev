#!/usr/bin/env python3
"""
Zoho Books Integration Investigation Test
Investigates why dashboard is showing dummy data instead of real Zoho Books data
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
    "name": "Zoho Investigation User",
    "email": "zohoinvestigation@test.com", 
    "password": "testpass123"
}

class ZohoInvestigationTester:
    def __init__(self):
        self.auth_token = None
        self.user_id = None
        self.mongo_client = None
        self.db = None
        
    def connect_to_mongodb(self):
        """Connect to MongoDB to investigate integration data"""
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
    
    def investigate_integration_status_in_db(self):
        """Step 1: Check integration status in MongoDB"""
        print("\n" + "="*60)
        print("📊 STEP 1: INVESTIGATING INTEGRATION STATUS IN DATABASE")
        print("="*60)
        
        if self.db is None:
            print("❌ No database connection")
            return None
            
        if not self.user_id:
            print("❌ No user ID available")
            return None
        
        try:
            # Query the integrations collection for this user
            integration = self.db.integrations.find_one({
                "user_id": self.user_id,
                "type": "zohobooks"
            })
            
            if integration:
                print("✅ Found Zoho Books integration in database:")
                print(f"   - User ID: {integration.get('user_id')}")
                print(f"   - Type: {integration.get('type')}")
                print(f"   - Mode: {integration.get('mode', 'NOT SET')}")
                print(f"   - Status: {integration.get('status', 'NOT SET')}")
                print(f"   - Email: {integration.get('email', 'NOT SET')}")
                print(f"   - Connected At: {integration.get('connected_at', 'NOT SET')}")
                print(f"   - Last Sync: {integration.get('last_sync', 'NOT SET')}")
                
                # Check for access token (redacted)
                access_token = integration.get('access_token')
                if access_token:
                    print(f"   - Access Token: {access_token[:10]}...{access_token[-10:]} (redacted)")
                else:
                    print("   - Access Token: NOT SET")
                
                # Check for client_id (redacted)
                client_id = integration.get('client_id')
                if client_id:
                    print(f"   - Client ID: {client_id[:10]}...{client_id[-10:]} (redacted)")
                else:
                    print("   - Client ID: NOT SET")
                
                print(f"\n🔍 ROOT CAUSE ANALYSIS:")
                
                # Check the critical condition from dashboard.py
                mode = integration.get("mode")
                status = integration.get("status")
                
                if mode != "production":
                    print(f"❌ ISSUE FOUND: Mode is '{mode}', but dashboard requires 'production'")
                    print("   This is why dashboard is showing mock data!")
                    
                if status != "active":
                    print(f"❌ ISSUE FOUND: Status is '{status}', but should be 'active'")
                    
                if mode == "production" and status == "active":
                    print("✅ Integration mode and status are correct for real data")
                    
                return integration
            else:
                print("❌ No Zoho Books integration found in database")
                print("   User has not connected Zoho Books yet")
                return None
                
        except Exception as e:
            print(f"❌ Error querying database: {str(e)}")
            return None
    
    def test_integration_status_api(self):
        """Test the integration status API endpoint"""
        print("\n" + "="*60)
        print("📊 STEP 2: TESTING INTEGRATION STATUS API")
        print("="*60)
        
        if not self.auth_token:
            print("❌ No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/integrations/status", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                print("✅ Integration Status API Response:")
                print(f"   - Zoho Books Connected: {data.get('zohobooks_connected', False)}")
                print(f"   - Zoho Books Email: {data.get('zohobooks_email', 'NOT SET')}")
                print(f"   - Last Sync: {data.get('last_sync', 'NOT SET')}")
                return data.get('zohobooks_connected', False)
            except json.JSONDecodeError:
                print("❌ Invalid JSON response from status API")
        else:
            print(f"❌ Status API failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def test_dashboard_collections_api(self):
        """Step 3: Test dashboard collections API to see what data it returns"""
        print("\n" + "="*60)
        print("📊 STEP 3: TESTING DASHBOARD COLLECTIONS API")
        print("="*60)
        
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
                print("✅ Dashboard Collections API Response:")
                print(f"   - Total Unpaid: {data.get('total_unpaid', 0)}")
                print(f"   - Total Overdue: {data.get('total_overdue', 0)}")
                print(f"   - Unpaid Invoices Count: {len(data.get('unpaid_invoices', []))}")
                print(f"   - Overdue Invoices Count: {len(data.get('overdue_invoices', []))}")
                
                # Check if this is mock data
                if data.get('total_unpaid') == 125000:  # Mock data value from dashboard.py
                    print("❌ CONFIRMED: API is returning MOCK DATA")
                    print("   This confirms the dashboard is not using real Zoho data")
                else:
                    print("✅ API appears to be returning real Zoho data")
                
                # Show sample invoice data
                unpaid_invoices = data.get('unpaid_invoices', [])
                if unpaid_invoices:
                    first_invoice = unpaid_invoices[0]
                    print(f"\n📋 Sample Invoice Data:")
                    print(f"   - Invoice Number: {first_invoice.get('invoice_number', 'N/A')}")
                    print(f"   - Customer: {first_invoice.get('customer_name', 'N/A')}")
                    print(f"   - Amount: {first_invoice.get('amount', 0)}")
                    
                    # Check for mock invoice numbers
                    if first_invoice.get('invoice_number') == 'INV-2024-001':
                        print("❌ CONFIRMED: This is mock invoice data")
                    else:
                        print("✅ This appears to be real invoice data")
                
                return True
            except json.JSONDecodeError:
                print("❌ Invalid JSON response from collections API")
        else:
            print(f"❌ Collections API failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def check_backend_logs(self):
        """Check backend logs for any Zoho API errors"""
        print("\n" + "="*60)
        print("📊 STEP 4: CHECKING BACKEND LOGS")
        print("="*60)
        
        try:
            import subprocess
            result = subprocess.run(
                ["tail", "-n", "50", "/var/log/supervisor/backend.err.log"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if result.returncode == 0:
                logs = result.stdout
                if logs.strip():
                    print("📋 Recent Backend Error Logs:")
                    print(logs)
                    
                    # Look for Zoho-related errors
                    if "zoho" in logs.lower() or "oauth" in logs.lower():
                        print("⚠️  Found Zoho/OAuth related errors in logs")
                    else:
                        print("✅ No obvious Zoho/OAuth errors in recent logs")
                else:
                    print("✅ No recent error logs found")
            else:
                print("❌ Could not read backend logs")
                
        except Exception as e:
            print(f"❌ Error reading logs: {str(e)}")
    
    def create_demo_integration_for_testing(self):
        """Create a demo integration to test the fix"""
        print("\n" + "="*60)
        print("📊 STEP 5: CREATING DEMO INTEGRATION FOR TESTING")
        print("="*60)
        
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
                    print(f"   - Integration ID: {data.get('integration_id')}")
                    return True
                else:
                    print(f"❌ Demo integration failed: {data.get('message', 'Unknown error')}")
            except json.JSONDecodeError:
                print("❌ Invalid JSON response from demo connect")
        else:
            print(f"❌ Demo connect failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def run_investigation(self):
        """Run the complete investigation"""
        print("🔍 ZOHO BOOKS INTEGRATION INVESTIGATION")
        print("Investigating why dashboard shows dummy data instead of real Zoho data")
        print("="*80)
        
        # Connect to MongoDB
        if not self.connect_to_mongodb():
            return False
        
        # Authenticate user
        if not self.authenticate_user():
            return False
        
        # Step 1: Check integration in database
        integration = self.investigate_integration_status_in_db()
        
        # Step 2: Test integration status API
        api_connected = self.test_integration_status_api()
        
        # Step 3: Test dashboard API
        dashboard_working = self.test_dashboard_collections_api()
        
        # Step 4: Check backend logs
        self.check_backend_logs()
        
        # Analysis and recommendations
        print("\n" + "="*80)
        print("🎯 INVESTIGATION SUMMARY & RECOMMENDATIONS")
        print("="*80)
        
        if not integration:
            print("❌ ROOT CAUSE: No Zoho Books integration found in database")
            print("📋 RECOMMENDATION: User needs to connect Zoho Books first")
            print("   - Use /api/integrations/zoho/demo-connect for demo mode")
            print("   - Use /api/integrations/zoho/user-oauth-setup for production mode")
            
            # Create demo integration for testing
            print("\n🔧 Creating demo integration for testing...")
            if self.create_demo_integration_for_testing():
                print("✅ Demo integration created. Re-testing dashboard...")
                self.test_dashboard_collections_api()
            
        elif integration.get("mode") != "production":
            mode = integration.get("mode", "NOT SET")
            print(f"❌ ROOT CAUSE: Integration mode is '{mode}', but dashboard requires 'production'")
            print("📋 RECOMMENDATION: Update integration mode to 'production'")
            print("   - This is the critical issue causing mock data to be shown")
            
            # Fix the mode in database
            print("\n🔧 Attempting to fix integration mode...")
            try:
                result = self.db.integrations.update_one(
                    {"user_id": self.user_id, "type": "zohobooks"},
                    {"$set": {"mode": "production"}}
                )
                if result.modified_count > 0:
                    print("✅ Updated integration mode to 'production'")
                    print("🔄 Re-testing dashboard API...")
                    self.test_dashboard_collections_api()
                else:
                    print("❌ Failed to update integration mode")
            except Exception as e:
                print(f"❌ Error updating integration: {str(e)}")
                
        elif integration.get("status") != "active":
            status = integration.get("status", "NOT SET")
            print(f"❌ ROOT CAUSE: Integration status is '{status}', but should be 'active'")
            print("📋 RECOMMENDATION: Update integration status to 'active'")
            
        elif not integration.get("access_token"):
            print("❌ ROOT CAUSE: No access token found in integration")
            print("📋 RECOMMENDATION: User needs to complete OAuth flow to get access token")
            
        else:
            print("✅ Integration appears to be configured correctly")
            print("📋 RECOMMENDATION: Check Zoho API connectivity and error handling")
            
        # Close MongoDB connection
        if self.mongo_client:
            self.mongo_client.close()
            
        return True

if __name__ == "__main__":
    investigator = ZohoInvestigationTester()
    success = investigator.run_investigation()
    sys.exit(0 if success else 1)