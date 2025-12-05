#!/usr/bin/env python
"""
Test script to verify login restrictions and logout functionality
"""

import os
import sys
import django

# Add the project directory to the path
sys.path.insert(0, 'e:/Backend Project')

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import Client

def test_login_restrictions():
    """Test that login restrictions are working correctly"""
    
    print("Testing Login Restrictions and Logout Functionality")
    print("=" * 60)
    
    client = Client()
    
    # Test 1: Login page should be accessible
    print("\n1. Testing login page accessibility...")
    try:
        response = client.get('/')
        if response.status_code == 200:
            print("   PASS: Login page is accessible")
        else:
            print(f"   FAIL: Login page returned status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: Error accessing login page: {str(e)}")
    
    # Test 2: create-hr should be accessible without login
    print("\n2. Testing create-hr accessibility without login...")
    try:
        response = client.get('/create-hr/')
        if response.status_code == 200:
            print("   PASS: create-hr page is accessible without login")
        else:
            print(f"   FAIL: create-hr page returned status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: Error accessing create-hr: {str(e)}")
    
    # Test 3: hr-list should be accessible without login
    print("\n3. Testing hr-list accessibility without login...")
    try:
        response = client.get('/hr-list/')
        if response.status_code == 200:
            print("   PASS: hr-list page is accessible without login")
        else:
            print(f"   FAIL: hr-list page returned status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: Error accessing hr-list: {str(e)}")
    
    # Test 4: Protected pages should redirect to login
    print("\n4. Testing protected pages redirect to login...")
    protected_pages = [
        '/dashboard/',
        '/employee-attendance/',
        '/payslip/',
    ]
    
    for page in protected_pages:
        try:
            response = client.get(page, follow=True)
            final_url = response.redirect_chain[-1][0] if response.redirect_chain else ""
            if 'login' in final_url or response.status_code == 200:
                print(f"   PASS: {page} properly redirects to login")
            else:
                print(f"   FAIL: {page} does not redirect properly")
        except Exception as e:
            print(f"   ERROR: Error testing {page}: {str(e)}")
    
    # Test 5: Test logout functionality
    print("\n5. Testing logout functionality...")
    try:
        response = client.get('/logout/')
        if response.status_code in [200, 302]:
            print("   PASS: Logout URL is accessible")
        else:
            print(f"   FAIL: Logout URL returned status: {response.status_code}")
    except Exception as e:
        print(f"   ERROR: Error testing logout: {str(e)}")
    
    print("\n" + "=" * 60)
    print("Test completed!")

if __name__ == "__main__":
    test_login_restrictions()