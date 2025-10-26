#!/usr/bin/env python3
"""
Zoho Books Integration Issue Investigation
Testing specific issues mentioned in review request
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

class ZohoIssueInvestigator:
    def __init__(self):
        self.auth_token = None
        self.findings = []
        
    def log_finding(self, issue, status, details):
        """Log investigation finding"""
        finding = {
            "issue": issue,
            "status": status,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        self.findings.append(finding)
        
        status_icon = "✅" if status == "RESOLVED" else "❌" if status == "CONFIRMED" else "⚠️"
        print(f"{status_icon} {issue}: {details}")
        
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
    
    def check_integration_status(self):
        """Check current integration status and mode"""
        if not self.auth_token:
            return None
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        response = self.make_request("GET", "/integrations/status", headers=headers)
        
        if response and response.status_code == 200:
            try:
                data = response.json()
                return data
            except json.JSONDecodeError:
                pass
        
        return None
    
    def get_integration_details_from_db(self):
        """Get detailed integration info including mode"""
        # This would require direct DB access, but we can infer from API responses
        # Let's check if we can get more details through other endpoints
        return None
    
    def test_chat_with_various_queries(self):
        """Test chat with different types of queries to check data fetching"""
        if not self.auth_token:
            self.log_finding("Chat Authentication", "FAILED", "No auth token available")
            return False
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        # Test queries mentioned in review request
        test_queries = [
            "Give me the latest invoice",
            "Show me my invoices", 
            "What are my invoice details?",
            "Show me overdue invoices",  # This should work based on current logic
            "Tell me about my outstanding payments",
            "What's my current financial status?"
        ]
        
        results = []
        
        for query in test_queries:
            chat_data = {"message": query}
            response = self.make_request("POST", "/chat/message", chat_data, headers)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    ai_response = data.get("response", "")
                    
                    # Check if response contains actual data or generic response
                    has_dummy_tag = "[DUMMY DATA]" in ai_response
                    has_specific_data = any(indicator in ai_response.lower() for indicator in [
                        "invoice", "₹", "amount", "customer", "overdue", "balance", "due"
                    ])
                    
                    results.append({
                        "query": query,
                        "response_length": len(ai_response),
                        "has_dummy_tag": has_dummy_tag,
                        "has_specific_data": has_specific_data,
                        "response_preview": ai_response[:200] + "..." if len(ai_response) > 200 else ai_response
                    })
                    
                except json.JSONDecodeError:
                    results.append({
                        "query": query,
                        "error": "Invalid JSON response"
                    })
            else:
                results.append({
                    "query": query,
                    "error": f"HTTP {response.status_code if response else 'No response'}"
                })
        
        return results
    
    def test_dashboard_data_source(self):
        """Test all dashboard endpoints to check if they return real or mock data"""
        if not self.auth_token:
            return {}
            
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.auth_token}"
        }
        
        endpoints = [
            "/dashboard/analytics",
            "/dashboard/collections", 
            "/dashboard/analytics-trends",
            "/dashboard/reconciliation"
        ]
        
        results = {}
        
        for endpoint in endpoints:
            response = self.make_request("GET", endpoint, headers=headers)
            
            if response and response.status_code == 200:
                try:
                    data = response.json()
                    
                    # Check for mock data indicators
                    is_mock_data = False
                    mock_indicators = []
                    
                    # Check for specific mock values
                    if endpoint == "/dashboard/analytics":
                        if data.get("total_outstanding") == 4520000:
                            is_mock_data = True
                            mock_indicators.append("total_outstanding=4520000 (mock value)")
                    
                    elif endpoint == "/dashboard/collections":
                        if data.get("total_unpaid") == 125000:
                            is_mock_data = True
                            mock_indicators.append("total_unpaid=125000 (mock value)")
                        
                        # Check for mock invoice numbers
                        unpaid = data.get("unpaid_invoices", [])
                        if unpaid and unpaid[0].get("invoice_number") == "INV-2024-001":
                            is_mock_data = True
                            mock_indicators.append("Mock invoice numbers (INV-2024-001)")
                    
                    elif endpoint == "/dashboard/analytics-trends":
                        if data.get("total_collected") == 6120000:
                            is_mock_data = True
                            mock_indicators.append("total_collected=6120000 (mock value)")
                    
                    elif endpoint == "/dashboard/reconciliation":
                        if data.get("total_matched") == 125000:
                            is_mock_data = True
                            mock_indicators.append("total_matched=125000 (mock value)")
                    
                    results[endpoint] = {
                        "status": "success",
                        "is_mock_data": is_mock_data,
                        "mock_indicators": mock_indicators,
                        "data_summary": {
                            "keys": list(data.keys()),
                            "sample_values": {k: v for k, v in list(data.items())[:3]}
                        }
                    }
                    
                except json.JSONDecodeError:
                    results[endpoint] = {"status": "error", "error": "Invalid JSON"}
            else:
                results[endpoint] = {"status": "error", "error": f"HTTP {response.status_code if response else 'No response'}"}
        
        return results
    
    def investigate_keyword_matching_issue(self):
        """Investigate the keyword matching issue in chat"""
        # Let's examine what keywords are currently supported
        # Based on the code review, the current logic in fetch_zoho_data_for_query only responds to:
        # ['invoice', 'overdue', 'outstanding', 'unpaid'] for invoices
        # ['customer', 'client', 'account'] for customers  
        # ['receivable', 'collection', 'summary', 'total'] for receivables
        
        current_keywords = {
            "invoice_keywords": ['invoice', 'overdue', 'outstanding', 'unpaid'],
            "customer_keywords": ['customer', 'client', 'account'],
            "receivable_keywords": ['receivable', 'collection', 'summary', 'total']
        }
        
        # Test queries that should work vs shouldn't work based on current logic
        should_work = [
            "Show me overdue invoices",  # contains 'overdue' and 'invoice'
            "What are my outstanding amounts?",  # contains 'outstanding'
            "Give me invoice details",  # contains 'invoice'
            "Show me unpaid invoices"  # contains 'unpaid' and 'invoice'
        ]
        
        might_not_work = [
            "Give me the latest invoice",  # contains 'invoice' but not specific status
            "Show me my invoices",  # contains 'invoice' but generic
            "What invoices do I have?",  # contains 'invoice' but generic
            "Tell me about my bills",  # doesn't contain any keywords
            "What's my financial status?"  # doesn't contain specific keywords
        ]
        
        return {
            "current_keywords": current_keywords,
            "should_work_queries": should_work,
            "might_not_work_queries": might_not_work,
            "issue_analysis": "The fetch_zoho_data_for_query function only fetches data for specific keywords. Generic queries like 'latest invoice' or 'show invoices' may not trigger data fetching."
        }
    
    def run_investigation(self):
        """Run complete investigation of Zoho integration issues"""
        print("🔍 Starting Zoho Books Integration Issue Investigation")
        print("=" * 70)
        
        # Step 1: Authenticate
        if not self.authenticate():
            self.log_finding("Authentication", "FAILED", "Could not authenticate user")
            return False
        
        print("\n1. CHECKING INTEGRATION STATUS")
        print("-" * 40)
        
        # Step 2: Check integration status
        status = self.check_integration_status()
        if status:
            connected = status.get("zohobooks_connected", False)
            email = status.get("zohobooks_email", "N/A")
            
            if connected:
                self.log_finding("Integration Status", "CONFIRMED", f"Zoho Books connected for {email}")
            else:
                self.log_finding("Integration Status", "ISSUE", "Zoho Books not connected")
        else:
            self.log_finding("Integration Status", "ERROR", "Could not retrieve integration status")
        
        print("\n2. TESTING CHAT DATA FETCHING")
        print("-" * 40)
        
        # Step 3: Test chat with various queries
        chat_results = self.test_chat_with_various_queries()
        
        # Analyze chat results
        working_queries = []
        failing_queries = []
        
        for result in chat_results:
            if "error" in result:
                failing_queries.append(result["query"])
                self.log_finding("Chat Query", "ERROR", f"'{result['query']}' - {result['error']}")
            else:
                if result["has_dummy_tag"]:
                    self.log_finding("Chat Query", "ISSUE", f"'{result['query']}' - Still showing [DUMMY DATA] tag")
                    failing_queries.append(result["query"])
                elif result["has_specific_data"]:
                    self.log_finding("Chat Query", "RESOLVED", f"'{result['query']}' - Returns specific data")
                    working_queries.append(result["query"])
                else:
                    self.log_finding("Chat Query", "PARTIAL", f"'{result['query']}' - Generic response, no specific data")
                    failing_queries.append(result["query"])
        
        print("\n3. TESTING DASHBOARD DATA SOURCE")
        print("-" * 40)
        
        # Step 4: Test dashboard endpoints
        dashboard_results = self.test_dashboard_data_source()
        
        mock_endpoints = []
        real_endpoints = []
        
        for endpoint, result in dashboard_results.items():
            if result["status"] == "success":
                if result["is_mock_data"]:
                    self.log_finding("Dashboard Data", "ISSUE", f"{endpoint} - Still showing mock data: {', '.join(result['mock_indicators'])}")
                    mock_endpoints.append(endpoint)
                else:
                    self.log_finding("Dashboard Data", "RESOLVED", f"{endpoint} - Using real/empty Zoho data")
                    real_endpoints.append(endpoint)
            else:
                self.log_finding("Dashboard Data", "ERROR", f"{endpoint} - {result['error']}")
        
        print("\n4. KEYWORD MATCHING ANALYSIS")
        print("-" * 40)
        
        # Step 5: Analyze keyword matching issue
        keyword_analysis = self.investigate_keyword_matching_issue()
        
        self.log_finding("Keyword Analysis", "INFO", keyword_analysis["issue_analysis"])
        
        print(f"\nCurrent supported keywords:")
        for category, keywords in keyword_analysis["current_keywords"].items():
            print(f"  {category}: {keywords}")
        
        print("\n" + "=" * 70)
        print("📊 INVESTIGATION SUMMARY")
        print("=" * 70)
        
        # Summary
        total_issues = len([f for f in self.findings if f["status"] in ["CONFIRMED", "ISSUE", "ERROR"]])
        total_resolved = len([f for f in self.findings if f["status"] == "RESOLVED"])
        
        print(f"Total Issues Found: {total_issues}")
        print(f"Total Resolved: {total_resolved}")
        
        print(f"\n🔍 KEY FINDINGS:")
        
        if status and status.get("zohobooks_connected"):
            print(f"  ✅ Zoho Books is connected")
        else:
            print(f"  ❌ Zoho Books connection issue")
        
        print(f"  📊 Chat queries working: {len(working_queries)}/{len(chat_results)}")
        print(f"  📊 Dashboard endpoints using real data: {len(real_endpoints)}/{len(dashboard_results)}")
        
        if failing_queries:
            print(f"\n❌ CHAT QUERIES NOT WORKING:")
            for query in failing_queries[:5]:  # Show first 5
                print(f"    - '{query}'")
        
        if mock_endpoints:
            print(f"\n❌ DASHBOARD ENDPOINTS STILL USING MOCK DATA:")
            for endpoint in mock_endpoints:
                print(f"    - {endpoint}")
        
        print(f"\n💡 RECOMMENDATIONS:")
        
        if failing_queries:
            print(f"  1. Expand keyword matching in fetch_zoho_data_for_query() to handle generic queries")
            print(f"  2. Consider always fetching Zoho data when user is connected, regardless of keywords")
        
        if mock_endpoints:
            print(f"  3. Check integration mode - ensure it's set to 'production' not 'demo'")
            print(f"  4. Verify Zoho API calls are succeeding and not falling back to mock data")
        
        # Detailed findings
        print(f"\n📋 DETAILED FINDINGS:")
        for finding in self.findings:
            status_icon = "✅" if finding["status"] == "RESOLVED" else "❌" if finding["status"] in ["CONFIRMED", "ISSUE", "ERROR"] else "⚠️"
            print(f"  {status_icon} {finding['issue']}: {finding['details']}")
        
        return total_issues == 0

if __name__ == "__main__":
    investigator = ZohoIssueInvestigator()
    success = investigator.run_investigation()
    sys.exit(0 if success else 1)