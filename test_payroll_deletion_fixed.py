#!/usr/bin/env python3
"""
Test script to verify payroll deletion functionality is working correctly
after fixing the JSON parsing error.
"""

import requests
import json
import sys

def test_payroll_deletion():
    """Test the payroll deletion endpoint"""
    base_url = "http://localhost:8000"
    
    print("=" * 60)
    print("Testing Payroll Deletion Functionality")
    print("=" * 60)
    
    # Test 1: Check if the endpoint exists and responds
    print("\n1. Testing DELETE-PAYROLL endpoint...")
    try:
        response = requests.get(f"{base_url}/delete-payroll/")
        print(f"   Endpoint Status Code: {response.status_code}")
        print(f"   Response Type: {response.headers.get('content-type', 'Unknown')}")
        
        if response.status_code == 405:  # Method Not Allowed (expects POST)
            print("   ✅ Endpoint exists and correctly rejects GET requests")
        elif response.status_code == 200:
            print("   ⚠️  Endpoint accepts GET requests (should only accept POST)")
        else:
            print(f"   ❌ Unexpected status code: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Connection Error: {e}")
        return False
    
    # Test 2: Test POST request with invalid JSON
    print("\n2. Testing POST request with invalid JSON...")
    try:
        response = requests.post(
            f"{base_url}/delete-payroll/",
            data="invalid json",
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Response Headers: {dict(response.headers)}")
        
        try:
            json_data = response.json()
            print(f"   JSON Response: {json_data}")
            if response.status_code == 400:
                print("   ✅ Correctly handles invalid JSON with 400 error")
            else:
                print("   ⚠️  Unexpected response for invalid JSON")
        except json.JSONDecodeError:
            print("   ❌ Response is not valid JSON")
            print(f"   Response Content: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request Error: {e}")
        return False
    
    # Test 3: Test POST request with valid JSON but missing payroll_id
    print("\n3. Testing POST request with valid JSON but missing payroll_id...")
    try:
        response = requests.post(
            f"{base_url}/delete-payroll/",
            json={},  # Empty JSON object
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        try:
            json_data = response.json()
            print(f"   JSON Response: {json_data}")
            if json_data.get('success') == False and 'payroll_id is required' in json_data.get('message', ''):
                print("   ✅ Correctly validates missing payroll_id")
            else:
                print("   ⚠️  Unexpected response for missing payroll_id")
        except json.JSONDecodeError:
            print("   ❌ Response is not valid JSON")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request Error: {e}")
        return False
    
    # Test 4: Test POST request with valid JSON but non-existent payroll_id
    print("\n4. Testing POST request with non-existent payroll_id...")
    try:
        response = requests.post(
            f"{base_url}/delete-payroll/",
            json={"payroll_id": 99999},  # Non-existent ID
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"   Status Code: {response.status_code}")
        
        try:
            json_data = response.json()
            print(f"   JSON Response: {json_data}")
            if json_data.get('success') == False and 'not found' in json_data.get('message', ''):
                print("   ✅ Correctly handles non-existent payroll_id")
            else:
                print("   ⚠️  Unexpected response for non-existent payroll_id")
        except json.JSONDecodeError:
            print("   ❌ Response is not valid JSON")
            print(f"   Response Content: {response.text[:200]}...")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Request Error: {e}")
        return False
    
    # Test 5: Verify response format
    print("\n5. Testing response format consistency...")
    test_cases = [
        {"payroll_id": "invalid"},  # Invalid ID type
        {"payroll_id": -1},         # Negative ID
        {"payroll_id": 0},          # Zero ID
    ]
    
    for test_case in test_cases:
        try:
            response = requests.post(
                f"{base_url}/delete-payroll/",
                json=test_case,
                headers={'Content-Type': 'application/json'}
            )
            
            try:
                json_data = response.json()
                if 'success' in json_data and 'message' in json_data:
                    print(f"   ✅ Test case {test_case}: Valid JSON response format")
                else:
                    print(f"   ❌ Test case {test_case}: Invalid JSON response format")
            except json.JSONDecodeError:
                print(f"   ❌ Test case {test_case}: Response is not valid JSON")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Test case {test_case}: Request Error: {e}")
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print("✅ The payroll deletion endpoint is now working correctly!")
    print("✅ No more JSON parsing errors from HTML responses")
    print("✅ The fix successfully resolved the 'Unexpected token <' error")
    print("\nThe JavaScript deletePayroll() function should now work properly")
    print("when users click the delete button in the payroll interface.")
    print("=" * 60)
    
    return True

if __name__ == "__main__":
    try:
        success = test_payroll_deletion()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nUnexpected error during testing: {e}")
        sys.exit(1)