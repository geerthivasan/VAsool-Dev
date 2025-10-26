#!/usr/bin/env python3
"""
Test specific issues mentioned in review request
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://fintech-collector.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

# Test data
TEST_USER = {
    "email": "testbackend@test.com", 
    "password": "testpass123"
}

class SpecificIssuesTester:
    def __init__(self):
        self.auth_token = None
        
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
    
    def authenticate(self):
        """Authenticate and get token"""
        login_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        response = self.make_request("POST", "/auth/login", login_data)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                if data.get("success") and data.get("token"):
                    self.auth_token = data["token"]
                    return True
            except json.JSONDecodeError:
                pass
        
        return False
    
    def test_issue_1_chat_not_returning_invoice_data(self):
        """Test ISSUE 1: Chat not returning invoice data for generic queries"""
        print("\n🔍 TESTING ISSUE 1: Chat Not Returning Invoice Data")
        print("=" * 60)
        
        if not self.auth_token:
            print("❌ Authentication failed")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # Test the exact queries mentioned in the review request
        test_queries = [
            "Give me the latest invoice",
            "Show me my invoices", 
            "invoice details"
        ]
        
        print("Testing queries that should fetch invoice data:")
        
        for query in test_queries:
            print(f"\n📝 Query: '{query}'")
            
            chat_data = {"message": query}
            response = self.make_request("POST", "/chat/message", chat_data, headers)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    ai_response = data.get("response", "")
                    
                    print(f"   Response length: {len(ai_response)} characters")
                    print(f"   Response preview: {ai_response[:150]}...")
                    
                    # Check if it contains actual invoice data or just generic response
                    has_dummy_tag = "[DUMMY DATA]" in ai_response
                    has_invoice_data = any(indicator in ai_response.lower() for indicator in [
                        "invoice", "₹", "amount", "customer", "overdue", "balance", "due", "zoho"
                    ])
                    
                    print(f"   Contains [DUMMY DATA] tag: {has_dummy_tag}")
                    print(f"   Contains invoice-related data: {has_invoice_data}")
                    
                    if has_dummy_tag:
                        print("   ❌ ISSUE CONFIRMED: Still showing [DUMMY DATA] despite Zoho connection")
                    elif has_invoice_data:
                        print("   ✅ WORKING: Response contains invoice-related information")
                    else:
                        print("   ⚠️  PARTIAL: Generic response without specific data")
                        
                except json.JSONDecodeError:
                    print("   ❌ Invalid JSON response")
            else:
                print(f"   ❌ Request failed: {response.status_code if response else 'No response'}")
        
        return True
    
    def test_issue_2_dashboard_showing_dummy_data(self):
        """Test ISSUE 2: Dashboard showing dummy data instead of real Zoho data"""
        print("\n🔍 TESTING ISSUE 2: Dashboard Showing Dummy Data")
        print("=" * 60)
        
        if not self.auth_token:
            print("❌ Authentication failed")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # Test all dashboard endpoints mentioned in review request
        endpoints = [
            ("/dashboard/analytics", "Analytics"),
            ("/dashboard/collections", "Collections"), 
            ("/dashboard/analytics-trends", "Analytics Trends")
        ]
        
        print("Testing dashboard endpoints for real vs dummy data:")
        
        for endpoint, name in endpoints:
            print(f"\n📊 Testing {name} ({endpoint})")
            
            response = self.make_request("GET", endpoint, headers=headers)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check for specific mock data values
                    is_mock = False
                    mock_indicators = []
                    
                    if endpoint == "/dashboard/analytics":
                        if data.get("total_outstanding") == 4520000:
                            is_mock = True
                            mock_indicators.append("total_outstanding=4520000 (mock)")
                        if data.get("recovery_rate") == 68.0:
                            is_mock = True
                            mock_indicators.append("recovery_rate=68.0 (mock)")
                        if data.get("active_accounts") == 124:
                            is_mock = True
                            mock_indicators.append("active_accounts=124 (mock)")
                    
                    elif endpoint == "/dashboard/collections":
                        if data.get("total_unpaid") == 125000:
                            is_mock = True
                            mock_indicators.append("total_unpaid=125000 (mock)")
                        if data.get("total_overdue") == 210000:
                            is_mock = True
                            mock_indicators.append("total_overdue=210000 (mock)")
                        
                        # Check for mock invoice numbers
                        unpaid = data.get("unpaid_invoices", [])
                        if unpaid and unpaid[0].get("invoice_number") == "INV-2024-001":
                            is_mock = True
                            mock_indicators.append("Mock invoice numbers (INV-2024-001)")
                    
                    elif endpoint == "/dashboard/analytics-trends":
                        if data.get("total_collected") == 6120000:
                            is_mock = True
                            mock_indicators.append("total_collected=6120000 (mock)")
                        if data.get("collection_efficiency") == 75.5:
                            is_mock = True
                            mock_indicators.append("collection_efficiency=75.5 (mock)")
                    
                    print(f"   Data keys: {list(data.keys())}")
                    
                    if is_mock:
                        print(f"   ❌ ISSUE CONFIRMED: Using mock data")
                        for indicator in mock_indicators:
                            print(f"      - {indicator}")
                    else:
                        print(f"   ✅ WORKING: Using real/empty Zoho data")
                        # Show some sample values
                        sample_values = {}
                        for key in list(data.keys())[:3]:
                            sample_values[key] = data[key]
                        print(f"      Sample values: {sample_values}")
                        
                except json.JSONDecodeError:
                    print("   ❌ Invalid JSON response")
            else:
                print(f"   ❌ Request failed: {response.status_code if response else 'No response'}")
        
        return True
    
    def test_integration_status_details(self):
        """Get detailed integration status"""
        print("\n🔍 CHECKING INTEGRATION STATUS DETAILS")
        print("=" * 60)
        
        if not self.auth_token:
            print("❌ Authentication failed")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/integrations/status", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                
                print(f"Zoho Books Connected: {data.get('zohobooks_connected', False)}")
                print(f"Zoho Books Email: {data.get('zohobooks_email', 'N/A')}")
                print(f"Last Sync: {data.get('last_sync', 'N/A')}")
                
                if data.get('zohobooks_connected'):
                    print("✅ User has Zoho Books connected")
                    
                    # The issue might be that it's connected in demo mode
                    # or the access tokens are missing
                    print("\n💡 ANALYSIS:")
                    print("   - User shows as connected to Zoho Books")
                    print("   - But dashboard might still show mock data")
                    print("   - This suggests integration is in 'demo' mode or missing access tokens")
                    
                else:
                    print("❌ User does not have Zoho Books connected")
                
                return data
                
            except json.JSONDecodeError:
                print("❌ Invalid JSON response")
        else:
            print(f"❌ Request failed: {response.status_code if response else 'No response'}")
        
        return None
    
    def run_tests(self):
        """Run all specific issue tests"""
        print("🚀 Testing Specific Issues from Review Request")
        print("=" * 70)
        
        # Authenticate first
        if not self.authenticate():
            print("❌ Authentication failed - cannot proceed with tests")
            return False
        
        print("✅ Authentication successful")
        
        # Get integration status first
        integration_status = self.test_integration_status_details()
        
        # Test Issue 1: Chat not returning invoice data
        self.test_issue_1_chat_not_returning_invoice_data()
        
        # Test Issue 2: Dashboard showing dummy data
        self.test_issue_2_dashboard_showing_dummy_data()
        
        print("\n" + "=" * 70)
        print("📋 SUMMARY OF FINDINGS")
        print("=" * 70)
        
        if integration_status and integration_status.get('zohobooks_connected'):
            print("✅ User has Zoho Books connected")
            print("\n🔍 ROOT CAUSE ANALYSIS:")
            print("   The issues are likely caused by:")
            print("   1. Integration is in 'demo' mode instead of 'production' mode")
            print("   2. Integration has no real access tokens (created via demo-connect)")
            print("   3. Dashboard code falls back to mock data when Zoho API calls fail")
            print("   4. Chat shows real responses because it checks connection status differently")
            
            print("\n💡 RECOMMENDED FIXES:")
            print("   1. Ensure integration mode is set to 'production' in database")
            print("   2. Verify integration has valid access_token and refresh_token")
            print("   3. Add better error logging to identify Zoho API failures")
            print("   4. Test with real Zoho OAuth flow instead of demo-connect")
        else:
            print("❌ User does not have Zoho Books connected")
            print("   This explains why dummy data is shown")
        
        return True

if __name__ == "__main__":
    tester = SpecificIssuesTester()
    success = tester.run_tests()
    sys.exit(0 if success else 1)