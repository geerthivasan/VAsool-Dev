#!/usr/bin/env python3
"""
Backend API Testing for Vasool Clone Application
Tests all authentication, demo, contact, chat, and dashboard APIs
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "https://fintech-collector.preview.emergentagent.com"
API_BASE = f"{BASE_URL}/api"

# Test data as specified in review request
TEST_USER = {
    "name": "Backend Test User",
    "email": "testbackend@test.com", 
    "password": "testpass123"
}

class VasoolAPITester:
    def __init__(self):
        self.auth_token = None
        self.session_id = None
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
    
    def test_auth_signup(self):
        """Test user registration"""
        print("\n=== Testing Authentication APIs ===")
        
        response = self.make_request("POST", "/auth/signup", TEST_USER)
        
        if response is None:
            self.log_result("Auth Signup", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success"):
                    self.log_result("Auth Signup", True, "User registered successfully", data)
                    return True
                else:
                    self.log_result("Auth Signup", False, f"Registration failed: {data.get('message', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Auth Signup", False, "Invalid JSON response")
        elif response.status_code == 400:
            # User might already exist, which is acceptable for testing
            try:
                data = response.json()
                if "already registered" in data.get("detail", "").lower():
                    self.log_result("Auth Signup", True, "User already exists (acceptable for testing)", data)
                    return True
                else:
                    self.log_result("Auth Signup", False, f"Bad request: {data.get('detail', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Auth Signup", False, f"Bad request with status {response.status_code}")
        else:
            self.log_result("Auth Signup", False, f"Unexpected status code: {response.status_code}")
            
        return False
    
    def test_auth_login(self):
        """Test user login"""
        login_data = {
            "email": TEST_USER["email"],
            "password": TEST_USER["password"]
        }
        
        response = self.make_request("POST", "/auth/login", login_data)
        
        if response is None:
            self.log_result("Auth Login", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success") and data.get("token"):
                    self.auth_token = data["token"]
                    self.log_result("Auth Login", True, "Login successful, token received", {
                        "user": data.get("user"),
                        "token_length": len(self.auth_token)
                    })
                    return True
                else:
                    self.log_result("Auth Login", False, "Login response missing success or token")
            except json.JSONDecodeError:
                self.log_result("Auth Login", False, "Invalid JSON response")
        else:
            try:
                error_data = response.json()
                self.log_result("Auth Login", False, f"Login failed: {error_data.get('detail', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Auth Login", False, f"Login failed with status {response.status_code}")
                
        return False
    
    def test_auth_me(self):
        """Test getting current user info"""
        if not self.auth_token:
            self.log_result("Auth Me", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/auth/me", headers=headers)
        
        if response is None:
            self.log_result("Auth Me", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("id") and data.get("email") == TEST_USER["email"]:
                    self.log_result("Auth Me", True, "User info retrieved successfully", data)
                    return True
                else:
                    self.log_result("Auth Me", False, "Invalid user data returned")
            except json.JSONDecodeError:
                self.log_result("Auth Me", False, "Invalid JSON response")
        else:
            self.log_result("Auth Me", False, f"Failed with status {response.status_code}")
            
        return False
    
    def test_demo_schedule(self):
        """Test demo scheduling"""
        print("\n=== Testing Demo & Contact APIs ===")
        
        demo_data = {
            "name": "John Demo User",
            "email": "demo@testcompany.com",
            "company": "Test Company Ltd",
            "phone": "+1-555-0123"
        }
        
        response = self.make_request("POST", "/demo/schedule", demo_data)
        
        if response is None:
            self.log_result("Demo Schedule", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success"):
                    self.log_result("Demo Schedule", True, "Demo scheduled successfully", data)
                    return True
                else:
                    self.log_result("Demo Schedule", False, f"Demo scheduling failed: {data.get('message', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Demo Schedule", False, "Invalid JSON response")
        else:
            self.log_result("Demo Schedule", False, f"Failed with status {response.status_code}")
            
        return False
    
    def test_contact_sales(self):
        """Test contact sales"""
        contact_data = {
            "name": "Jane Contact User",
            "email": "contact@testcompany.com",
            "message": "I'm interested in learning more about your collections platform and would like to discuss pricing options for our organization."
        }
        
        response = self.make_request("POST", "/contact/sales", contact_data)
        
        if response is None:
            self.log_result("Contact Sales", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("success"):
                    self.log_result("Contact Sales", True, "Contact message sent successfully", data)
                    return True
                else:
                    self.log_result("Contact Sales", False, f"Contact failed: {data.get('message', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Contact Sales", False, "Invalid JSON response")
        else:
            self.log_result("Contact Sales", False, f"Failed with status {response.status_code}")
            
        return False
    
    def test_chat_message(self):
        """Test sending chat message"""
        print("\n=== Testing Chat APIs ===")
        
        if not self.auth_token:
            self.log_result("Chat Message", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # Test different types of messages to verify AI responses
        test_messages = [
            "Can you help me analyze my collections portfolio?",
            "I need to track payment activities for this month",
            "What strategies do you recommend for optimizing collections?"
        ]
        
        success_count = 0
        
        for i, message in enumerate(test_messages):
            chat_data = {"message": message}
            
            response = self.make_request("POST", "/chat/message", chat_data, headers)
            
            if response is None:
                self.log_result(f"Chat Message {i+1}", False, "Request failed - connection error")
                continue
                
            if response.status_code == 200:
                try:
                    data = response.json()
                    if data.get("response") and data.get("session_id"):
                        if not self.session_id:
                            self.session_id = data["session_id"]
                        self.log_result(f"Chat Message {i+1}", True, f"AI responded: {data['response'][:100]}...", {
                            "session_id": data["session_id"],
                            "response_length": len(data["response"])
                        })
                        success_count += 1
                    else:
                        self.log_result(f"Chat Message {i+1}", False, "Invalid response format")
                except json.JSONDecodeError:
                    self.log_result(f"Chat Message {i+1}", False, "Invalid JSON response")
            else:
                self.log_result(f"Chat Message {i+1}", False, f"Failed with status {response.status_code}")
        
        return success_count > 0
    
    def test_chat_history(self):
        """Test retrieving chat history"""
        if not self.auth_token:
            self.log_result("Chat History", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # Test without session_id (should return default message)
        response = self.make_request("GET", "/chat/history", headers=headers)
        
        if response is None:
            self.log_result("Chat History", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get("messages") and isinstance(data["messages"], list):
                    self.log_result("Chat History", True, f"Retrieved {len(data['messages'])} messages", {
                        "message_count": len(data["messages"]),
                        "first_message": data["messages"][0] if data["messages"] else None
                    })
                    return True
                else:
                    self.log_result("Chat History", False, "Invalid history format")
            except json.JSONDecodeError:
                self.log_result("Chat History", False, "Invalid JSON response")
        else:
            self.log_result("Chat History", False, f"Failed with status {response.status_code}")
            
        return False
    
    def test_dashboard_analytics(self):
        """Test dashboard analytics"""
        print("\n=== Testing Dashboard APIs ===")
        
        if not self.auth_token:
            self.log_result("Dashboard Analytics", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/analytics", headers=headers)
        
        if response is None:
            self.log_result("Dashboard Analytics", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["total_outstanding", "recovery_rate", "active_accounts", "recent_activity"]
                
                if all(field in data for field in required_fields):
                    self.log_result("Dashboard Analytics", True, "Analytics data retrieved successfully", {
                        "total_outstanding": data["total_outstanding"],
                        "recovery_rate": data["recovery_rate"],
                        "active_accounts": data["active_accounts"],
                        "activity_count": len(data["recent_activity"])
                    })
                    return True
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("Dashboard Analytics", False, f"Missing required fields: {missing_fields}")
            except json.JSONDecodeError:
                self.log_result("Dashboard Analytics", False, "Invalid JSON response")
        else:
            self.log_result("Dashboard Analytics", False, f"Failed with status {response.status_code}")
            
        return False

    def test_dashboard_collections(self):
        """Test dashboard collections endpoint"""
        if not self.auth_token:
            self.log_result("Dashboard Collections", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/collections", headers=headers)
        
        if response is None:
            self.log_result("Dashboard Collections", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["unpaid_invoices", "overdue_invoices", "total_unpaid", "total_overdue"]
                
                if all(field in data for field in required_fields):
                    # Verify data structure
                    unpaid_count = len(data["unpaid_invoices"])
                    overdue_count = len(data["overdue_invoices"])
                    
                    # Check if invoice items have required fields
                    valid_structure = True
                    if unpaid_count > 0:
                        first_unpaid = data["unpaid_invoices"][0]
                        invoice_fields = ["id", "invoice_number", "customer_name", "amount", "balance", "due_date", "status"]
                        if not all(field in first_unpaid for field in invoice_fields):
                            valid_structure = False
                    
                    if valid_structure:
                        self.log_result("Dashboard Collections", True, "Collections data retrieved successfully", {
                            "unpaid_count": unpaid_count,
                            "overdue_count": overdue_count,
                            "total_unpaid": data["total_unpaid"],
                            "total_overdue": data["total_overdue"]
                        })
                        return True
                    else:
                        self.log_result("Dashboard Collections", False, "Invalid invoice item structure")
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("Dashboard Collections", False, f"Missing required fields: {missing_fields}")
            except json.JSONDecodeError:
                self.log_result("Dashboard Collections", False, "Invalid JSON response")
        else:
            self.log_result("Dashboard Collections", False, f"Failed with status {response.status_code}")
            
        return False

    def test_dashboard_analytics_trends(self):
        """Test dashboard analytics trends endpoint"""
        if not self.auth_token:
            self.log_result("Dashboard Analytics Trends", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/analytics-trends", headers=headers)
        
        if response is None:
            self.log_result("Dashboard Analytics Trends", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["monthly_trends", "total_collected", "total_outstanding", "collection_efficiency", "average_collection_time"]
                
                if all(field in data for field in required_fields):
                    # Verify monthly trends structure
                    trends_count = len(data["monthly_trends"])
                    valid_trends = True
                    
                    if trends_count > 0:
                        first_trend = data["monthly_trends"][0]
                        trend_fields = ["month", "collected", "outstanding"]
                        if not all(field in first_trend for field in trend_fields):
                            valid_trends = False
                    
                    if valid_trends:
                        self.log_result("Dashboard Analytics Trends", True, "Analytics trends data retrieved successfully", {
                            "trends_count": trends_count,
                            "total_collected": data["total_collected"],
                            "total_outstanding": data["total_outstanding"],
                            "collection_efficiency": data["collection_efficiency"],
                            "average_collection_time": data["average_collection_time"]
                        })
                        return True
                    else:
                        self.log_result("Dashboard Analytics Trends", False, "Invalid monthly trends structure")
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("Dashboard Analytics Trends", False, f"Missing required fields: {missing_fields}")
            except json.JSONDecodeError:
                self.log_result("Dashboard Analytics Trends", False, "Invalid JSON response")
        else:
            self.log_result("Dashboard Analytics Trends", False, f"Failed with status {response.status_code}")
            
        return False

    def test_dashboard_reconciliation(self):
        """Test dashboard reconciliation endpoint"""
        if not self.auth_token:
            self.log_result("Dashboard Reconciliation", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/dashboard/reconciliation", headers=headers)
        
        if response is None:
            self.log_result("Dashboard Reconciliation", False, "Request failed - connection error")
            return False
            
        if response.status_code == 200:
            try:
                data = response.json()
                required_fields = ["matched_items", "unmatched_items", "total_matched", "total_unmatched"]
                
                if all(field in data for field in required_fields):
                    # Verify reconciliation items structure
                    matched_count = len(data["matched_items"])
                    unmatched_count = len(data["unmatched_items"])
                    
                    valid_structure = True
                    if matched_count > 0:
                        first_matched = data["matched_items"][0]
                        item_fields = ["id", "date", "description", "amount", "status"]
                        if not all(field in first_matched for field in item_fields):
                            valid_structure = False
                    
                    if valid_structure:
                        self.log_result("Dashboard Reconciliation", True, "Reconciliation data retrieved successfully", {
                            "matched_count": matched_count,
                            "unmatched_count": unmatched_count,
                            "total_matched": data["total_matched"],
                            "total_unmatched": data["total_unmatched"]
                        })
                        return True
                    else:
                        self.log_result("Dashboard Reconciliation", False, "Invalid reconciliation item structure")
                else:
                    missing_fields = [field for field in required_fields if field not in data]
                    self.log_result("Dashboard Reconciliation", False, f"Missing required fields: {missing_fields}")
            except json.JSONDecodeError:
                self.log_result("Dashboard Reconciliation", False, "Invalid JSON response")
        else:
            self.log_result("Dashboard Reconciliation", False, f"Failed with status {response.status_code}")
            
        return False

    def test_validation_error_handling(self):
        """Test validation error handling - should return user-friendly string messages"""
        print("\n=== Testing Validation Error Handling ===")
        
        if not self.auth_token:
            self.log_result("Validation Error Handling", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # Test with invalid/missing data for user-oauth-setup endpoint
        invalid_data = {}  # Missing required fields should trigger validation error
        
        response = self.make_request("POST", "/integrations/zoho/user-oauth-setup", invalid_data, headers)
        
        if response is None:
            self.log_result("Validation Error Handling", False, "Request failed - connection error")
            return False
            
        if response.status_code == 422:  # Validation error expected
            try:
                data = response.json()
                
                # Check if response has user-friendly error format
                if "detail" in data and isinstance(data["detail"], str):
                    # Should be a simple string, not a complex object
                    error_message = data["detail"]
                    
                    # Verify it's not the old Pydantic format with type, loc, msg, etc.
                    if not any(key in str(data) for key in ["type", "loc", "msg", "input", "url"]):
                        self.log_result("Validation Error Handling", True, f"User-friendly error message returned: {error_message}", {
                            "error_message": error_message,
                            "response_format": "simple_string"
                        })
                        return True
                    else:
                        self.log_result("Validation Error Handling", False, "Error response still contains complex Pydantic format")
                else:
                    self.log_result("Validation Error Handling", False, f"Error response format not user-friendly: {data}")
            except json.JSONDecodeError:
                self.log_result("Validation Error Handling", False, "Invalid JSON response")
        else:
            self.log_result("Validation Error Handling", False, f"Expected validation error (422), got status {response.status_code}")
            
        return False

    def test_zoho_oauth_setup(self):
        """Test Zoho OAuth setup endpoint with user-provided credentials"""
        print("\n=== Testing Zoho OAuth Setup ===")
        
        if not self.auth_token:
            self.log_result("Zoho OAuth Setup", False, "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # Test credentials provided by user
        test_credentials = {
            "client_id": "1000.OH8JNIK1UP8VEGHLM6QN4BC6CM801K",
            "client_secret": "c7ff157ccf95db7751ed218370973cf86db0477597"
        }
        
        success_count = 0
        total_tests = 3
        
        # Test 1: organization_id as empty string
        test_data_1 = {**test_credentials, "organization_id": ""}
        response = self.make_request("POST", "/integrations/zoho/user-oauth-setup", test_data_1, headers)
        
        if response is None:
            self.log_result("Zoho OAuth Setup (empty org_id)", False, "Request failed - connection error")
        elif response.status_code == 200:
            try:
                data = response.json()
                if data.get("auth_url") and data.get("state"):
                    if "zoho" in data["auth_url"].lower() and "oauth" in data["auth_url"].lower():
                        self.log_result("Zoho OAuth Setup (empty org_id)", True, "Valid auth URL and state returned", {
                            "auth_url_length": len(data["auth_url"]),
                            "state_length": len(data["state"]),
                            "contains_client_id": test_credentials["client_id"] in data["auth_url"]
                        })
                        success_count += 1
                    else:
                        self.log_result("Zoho OAuth Setup (empty org_id)", False, "Auth URL doesn't appear to be valid Zoho OAuth URL")
                else:
                    self.log_result("Zoho OAuth Setup (empty org_id)", False, "Missing auth_url or state in response")
            except json.JSONDecodeError:
                self.log_result("Zoho OAuth Setup (empty org_id)", False, "Invalid JSON response")
        else:
            try:
                error_data = response.json()
                self.log_result("Zoho OAuth Setup (empty org_id)", False, f"Failed with status {response.status_code}: {error_data.get('detail', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Zoho OAuth Setup (empty org_id)", False, f"Failed with status {response.status_code}")
        
        # Test 2: organization_id not included in request
        test_data_2 = test_credentials.copy()  # No organization_id field
        response = self.make_request("POST", "/integrations/zoho/user-oauth-setup", test_data_2, headers)
        
        if response is None:
            self.log_result("Zoho OAuth Setup (no org_id)", False, "Request failed - connection error")
        elif response.status_code == 200:
            try:
                data = response.json()
                if data.get("auth_url") and data.get("state"):
                    if "zoho" in data["auth_url"].lower() and "oauth" in data["auth_url"].lower():
                        self.log_result("Zoho OAuth Setup (no org_id)", True, "Valid auth URL and state returned", {
                            "auth_url_length": len(data["auth_url"]),
                            "state_length": len(data["state"]),
                            "contains_client_id": test_credentials["client_id"] in data["auth_url"]
                        })
                        success_count += 1
                    else:
                        self.log_result("Zoho OAuth Setup (no org_id)", False, "Auth URL doesn't appear to be valid Zoho OAuth URL")
                else:
                    self.log_result("Zoho OAuth Setup (no org_id)", False, "Missing auth_url or state in response")
            except json.JSONDecodeError:
                self.log_result("Zoho OAuth Setup (no org_id)", False, "Invalid JSON response")
        else:
            try:
                error_data = response.json()
                self.log_result("Zoho OAuth Setup (no org_id)", False, f"Failed with status {response.status_code}: {error_data.get('detail', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Zoho OAuth Setup (no org_id)", False, f"Failed with status {response.status_code}")
        
        # Test 3: organization_id as null
        test_data_3 = {**test_credentials, "organization_id": None}
        response = self.make_request("POST", "/integrations/zoho/user-oauth-setup", test_data_3, headers)
        
        if response is None:
            self.log_result("Zoho OAuth Setup (null org_id)", False, "Request failed - connection error")
        elif response.status_code == 200:
            try:
                data = response.json()
                if data.get("auth_url") and data.get("state"):
                    if "zoho" in data["auth_url"].lower() and "oauth" in data["auth_url"].lower():
                        self.log_result("Zoho OAuth Setup (null org_id)", True, "Valid auth URL and state returned", {
                            "auth_url_length": len(data["auth_url"]),
                            "state_length": len(data["state"]),
                            "contains_client_id": test_credentials["client_id"] in data["auth_url"]
                        })
                        success_count += 1
                    else:
                        self.log_result("Zoho OAuth Setup (null org_id)", False, "Auth URL doesn't appear to be valid Zoho OAuth URL")
                else:
                    self.log_result("Zoho OAuth Setup (null org_id)", False, "Missing auth_url or state in response")
            except json.JSONDecodeError:
                self.log_result("Zoho OAuth Setup (null org_id)", False, "Invalid JSON response")
        else:
            try:
                error_data = response.json()
                self.log_result("Zoho OAuth Setup (null org_id)", False, f"Failed with status {response.status_code}: {error_data.get('detail', 'Unknown error')}")
            except json.JSONDecodeError:
                self.log_result("Zoho OAuth Setup (null org_id)", False, f"Failed with status {response.status_code}")
        
        return success_count == total_tests
    
    def run_all_tests(self):
        """Run all API tests"""
        print("🚀 Starting Vasool Backend API Tests")
        print(f"Testing against: {BASE_URL}")
        print("=" * 60)
        
        # Authentication flow
        signup_success = self.test_auth_signup()
        login_success = self.test_auth_login()
        me_success = self.test_auth_me()
        
        # Public APIs
        demo_success = self.test_demo_schedule()
        contact_success = self.test_contact_sales()
        
        # Authenticated APIs
        chat_success = self.test_chat_message()
        history_success = self.test_chat_history()
        dashboard_success = self.test_dashboard_analytics()
        
        # NEW: Dashboard endpoints testing
        collections_success = self.test_dashboard_collections()
        analytics_trends_success = self.test_dashboard_analytics_trends()
        reconciliation_success = self.test_dashboard_reconciliation()
        
        # Validation error handling
        validation_success = self.test_validation_error_handling()
        
        # Summary
        print("\n" + "=" * 60)
        print("📊 TEST SUMMARY")
        print("=" * 60)
        
        total_tests = len(self.test_results)
        passed_tests = sum(1 for result in self.test_results if result["success"])
        
        print(f"Total Tests: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {total_tests - passed_tests}")
        print(f"Success Rate: {(passed_tests/total_tests)*100:.1f}%")
        
        # Critical failures
        critical_failures = []
        if not login_success:
            critical_failures.append("Authentication login failed")
        if not (chat_success or history_success):
            critical_failures.append("Chat functionality completely broken")
        if not dashboard_success:
            critical_failures.append("Dashboard analytics not working")
        if not (collections_success and analytics_trends_success and reconciliation_success):
            critical_failures.append("New dashboard endpoints not working properly")
        if not validation_success:
            critical_failures.append("Validation error handling not user-friendly")
            
        if critical_failures:
            print("\n🚨 CRITICAL ISSUES:")
            for failure in critical_failures:
                print(f"  - {failure}")
        
        # Detailed results
        print("\n📋 DETAILED RESULTS:")
        for result in self.test_results:
            status = "✅" if result["success"] else "❌"
            print(f"  {status} {result['test']}: {result['message']}")
        
        return passed_tests == total_tests

if __name__ == "__main__":
    tester = VasoolAPITester()
    success = tester.run_all_tests()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)