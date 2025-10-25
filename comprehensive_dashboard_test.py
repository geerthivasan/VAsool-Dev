#!/usr/bin/env python3
"""
Comprehensive Dashboard Test - Test all dashboard endpoints with Zoho integration
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://fintech-collector.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

# Test user credentials
TEST_USER = {
    "name": "Dashboard Test User",
    "email": "dashboardtest@test.com", 
    "password": "testpass123"
}

class DashboardTester:
    def __init__(self):
        self.auth_token = None
        self.test_results = []
        
    def log_result(self, test_name, success, message, response_data=None):
        """Log test result"""
        result = {
            "test": test_name,
            "success": success,
            "message": message,
            "timestamp": datetime.now().isoformat()
        }
        if response_data:
            result["response_data"] = response_data
        self.test_results.append(result)
        
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}: {message}")
        
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
                    print(f"✅ Authentication successful")
                    return True
                else:
                    print("❌ Login response missing success or token")
            except json.JSONDecodeError:
                print("❌ Invalid JSON response from login")
        else:
            print(f"❌ Login failed with status {login_response.status_code if login_response else 'None'}")
            
        return False
    
    def create_demo_integration(self):
        """Create demo integration for testing"""
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
    
    def test_integration_status(self):
        """Test integration status endpoint"""
        print("\n=== Testing Integration Status ===")
        
        if not self.auth_token:
            self.log_result("Integration Status", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/integrations/status", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                zoho_connected = data.get('zohobooks_connected', False)
                
                if zoho_connected:
                    self.log_result("Integration Status", True, 
                                  f"Zoho Books connected: {data.get('zohobooks_email', 'N/A')}", data)
                    return True
                else:
                    self.log_result("Integration Status", True, "Zoho Books not connected", data)
                    return False
            except json.JSONDecodeError:
                self.log_result("Integration Status", False, "Invalid JSON response")
        else:
            self.log_result("Integration Status", False, f"Failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def test_dashboard_analytics(self):
        """Test dashboard analytics endpoint"""
        print("\n=== Testing Dashboard Analytics ===")
        
        if not self.auth_token:
            self.log_result("Dashboard Analytics", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/analytics", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["total_outstanding", "recovery_rate", "active_accounts", "recent_activity"]
                
                if all(field in data for field in required_fields):
                    # Check if this is mock data or real data
                    is_mock_data = data.get("total_outstanding") == 4520000
                    data_type = "mock" if is_mock_data else "real/empty"
                    
                    self.log_result("Dashboard Analytics", True, 
                                  f"Analytics data retrieved ({data_type}): Outstanding={data['total_outstanding']}, Rate={data['recovery_rate']}%, Accounts={data['active_accounts']}", {
                        "total_outstanding": data["total_outstanding"],
                        "recovery_rate": data["recovery_rate"],
                        "active_accounts": data["active_accounts"],
                        "activity_count": len(data["recent_activity"]),
                        "data_type": data_type
                    })
                    return True
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("Dashboard Analytics", False, f"Missing required fields: {missing_fields}")
            except json.JSONDecodeError:
                self.log_result("Dashboard Analytics", False, "Invalid JSON response")
        else:
            self.log_result("Dashboard Analytics", False, f"Failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def test_dashboard_collections(self):
        """Test dashboard collections endpoint"""
        print("\n=== Testing Dashboard Collections ===")
        
        if not self.auth_token:
            self.log_result("Dashboard Collections", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/collections", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["unpaid_invoices", "overdue_invoices", "total_unpaid", "total_overdue"]
                
                if all(field in data for field in required_fields):
                    # Check if this is mock data or real data
                    is_mock_data = data.get("total_unpaid") == 125000
                    data_type = "mock" if is_mock_data else "real/empty"
                    
                    unpaid_count = len(data["unpaid_invoices"])
                    overdue_count = len(data["overdue_invoices"])
                    
                    self.log_result("Dashboard Collections", True, 
                                  f"Collections data retrieved ({data_type}): {unpaid_count} unpaid, {overdue_count} overdue, Total unpaid: {data['total_unpaid']}", {
                        "unpaid_count": unpaid_count,
                        "overdue_count": overdue_count,
                        "total_unpaid": data["total_unpaid"],
                        "total_overdue": data["total_overdue"],
                        "data_type": data_type
                    })
                    return True
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("Dashboard Collections", False, f"Missing required fields: {missing_fields}")
            except json.JSONDecodeError:
                self.log_result("Dashboard Collections", False, "Invalid JSON response")
        else:
            self.log_result("Dashboard Collections", False, f"Failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def test_dashboard_analytics_trends(self):
        """Test dashboard analytics trends endpoint"""
        print("\n=== Testing Dashboard Analytics Trends ===")
        
        if not self.auth_token:
            self.log_result("Dashboard Analytics Trends", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/analytics-trends", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["monthly_trends", "total_collected", "total_outstanding", "collection_efficiency", "average_collection_time"]
                
                if all(field in data for field in required_fields):
                    # Check if this is mock data or real data
                    is_mock_data = data.get("total_collected") == 6120000
                    data_type = "mock" if is_mock_data else "real/empty"
                    
                    trends_count = len(data["monthly_trends"])
                    
                    self.log_result("Dashboard Analytics Trends", True, 
                                  f"Analytics trends data retrieved ({data_type}): {trends_count} months, Collected: {data['total_collected']}, Efficiency: {data['collection_efficiency']}%", {
                        "trends_count": trends_count,
                        "total_collected": data["total_collected"],
                        "total_outstanding": data["total_outstanding"],
                        "collection_efficiency": data["collection_efficiency"],
                        "average_collection_time": data["average_collection_time"],
                        "data_type": data_type
                    })
                    return True
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("Dashboard Analytics Trends", False, f"Missing required fields: {missing_fields}")
            except json.JSONDecodeError:
                self.log_result("Dashboard Analytics Trends", False, "Invalid JSON response")
        else:
            self.log_result("Dashboard Analytics Trends", False, f"Failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def test_dashboard_reconciliation(self):
        """Test dashboard reconciliation endpoint"""
        print("\n=== Testing Dashboard Reconciliation ===")
        
        if not self.auth_token:
            self.log_result("Dashboard Reconciliation", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/reconciliation", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["matched_items", "unmatched_items", "total_matched", "total_unmatched"]
                
                if all(field in data for field in required_fields):
                    # Check if this is mock data or real data
                    is_mock_data = data.get("total_matched") == 125000
                    data_type = "mock" if is_mock_data else "real/empty"
                    
                    matched_count = len(data["matched_items"])
                    unmatched_count = len(data["unmatched_items"])
                    
                    self.log_result("Dashboard Reconciliation", True, 
                                  f"Reconciliation data retrieved ({data_type}): {matched_count} matched, {unmatched_count} unmatched, Total matched: {data['total_matched']}", {
                        "matched_count": matched_count,
                        "unmatched_count": unmatched_count,
                        "total_matched": data["total_matched"],
                        "total_unmatched": data["total_unmatched"],
                        "data_type": data_type
                    })
                    return True
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("Dashboard Reconciliation", False, f"Missing required fields: {missing_fields}")
            except json.JSONDecodeError:
                self.log_result("Dashboard Reconciliation", False, "Invalid JSON response")
        else:
            self.log_result("Dashboard Reconciliation", False, f"Failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def test_chat_with_zoho_integration(self):
        """Test chat endpoint with Zoho integration"""
        print("\n=== Testing Chat with Zoho Integration ===")
        
        if not self.auth_token:
            self.log_result("Chat with Zoho Integration", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # Test message asking about invoices
        test_message = "Show me my overdue invoices and collections data"
        chat_data = {"message": test_message}
        
        response = self.make_request("POST", "/chat/message", chat_data, headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                ai_response = data.get("response", "")
                session_id = data.get("session_id")
                
                if not ai_response:
                    self.log_result("Chat with Zoho Integration", False, "No AI response received")
                    return False
                
                # Check if response contains [DUMMY DATA] tag
                has_dummy_tag = "[DUMMY DATA]" in ai_response
                
                # Since we have Zoho connected (even in demo mode), it should NOT have dummy tag
                if has_dummy_tag:
                    self.log_result("Chat with Zoho Integration", False, 
                                  f"Response incorrectly contains [DUMMY DATA] tag despite Zoho being connected. Response: {ai_response[:200]}...")
                    return False
                else:
                    self.log_result("Chat with Zoho Integration", True, 
                                  f"Chat response correctly shows no [DUMMY DATA] tag when Zoho connected. Response: {ai_response[:200]}...", {
                        "session_id": session_id,
                        "response_length": len(ai_response),
                        "contains_dummy_tag": False
                    })
                    return True
                    
            except json.JSONDecodeError:
                self.log_result("Chat with Zoho Integration", False, "Invalid JSON response")
        else:
            try:
                error_data = response.json() if response else {}
                self.log_result("Chat with Zoho Integration", False, f"Failed with status {response.status_code if response else 'None'}: {error_data.get('detail', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Chat with Zoho Integration", False, f"Failed with status {response.status_code if response else 'None'}")
            
        return False
    
    def run_comprehensive_test(self):
        """Run comprehensive dashboard test"""
        print("🚀 COMPREHENSIVE DASHBOARD TEST WITH ZOHO INTEGRATION")
        print("Testing all dashboard endpoints after fixing integration mode")
        print("="*80)
        
        # Authenticate user
        if not self.authenticate_user():
            return False
        
        # Create demo integration
        if not self.create_demo_integration():
            return False
        
        # Test integration status
        zoho_connected = self.test_integration_status()
        
        # Test all dashboard endpoints
        analytics_success = self.test_dashboard_analytics()
        collections_success = self.test_dashboard_collections()
        trends_success = self.test_dashboard_analytics_trends()
        reconciliation_success = self.test_dashboard_reconciliation()
        
        # Test chat integration
        chat_success = self.test_chat_with_zoho_integration()
        
        # Summary
        print("\n" + "="*80)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("="*80)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Key findings
        print(f"\n🔍 KEY FINDINGS:")
        print(f"  - Zoho Books Connected: {'Yes' if zoho_connected else 'No'}")
        print(f"  - Dashboard Analytics: {'✅ Working' if analytics_success else '❌ Failed'}")
        print(f"  - Dashboard Collections: {'✅ Working' if collections_success else '❌ Failed'}")
        print(f"  - Dashboard Trends: {'✅ Working' if trends_success else '❌ Failed'}")
        print(f"  - Dashboard Reconciliation: {'✅ Working' if reconciliation_success else '❌ Failed'}")
        print(f"  - Chat Integration: {'✅ Working' if chat_success else '❌ Failed'}")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {result['test']}: {result['message']}")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = DashboardTester()
    success = tester.run_comprehensive_test()
    sys.exit(0 if success else 1)