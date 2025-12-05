#!/usr/bin/env python3
"""
Simple test to verify login/logout behavior fixes
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manage')
django.setup()

def test_simple_auth():
    """Test basic authentication flow"""
    print("🧪 TESTING LOGIN/LOGOUT FIXES")
    print("=" * 40)
    
    try:
        from django.test import Client
        from app.models import Employee
        
        client = Client()
        
        # Test 1: Login page accessibility
        print("\n1. Testing login page...")
        response = client.get('/')
        print(f"   Status: {response.status_code} - {'✅' if response.status_code == 200 else '❌'}")
        
        # Test 2: Protected page without login
        print("\n2. Testing protected page redirect...")
        response = client.get('/employee-dashboard/')
        print(f"   Status: {response.status_code} - {'✅' if response.status_code == 302 else '❌'}")
        if response.status_code == 302:
            print(f"   Redirect to: {response.url}")
        
        # Test 3: Attendance table (should be accessible)
        print("\n3. Testing attendance table...")
        response = client.get('/attendance-table/')
        print(f"   Status: {response.status_code} - {'✅' if response.status_code == 200 else '❌'}")
        
        # Test 4: Create test user and test login
        print("\n4. Testing login flow...")
        try:
            test_emp = Employee.objects.create(
                first_name="Test",
                last_name="User", 
                email="test@example.com",
                password="password123",
                company_id="TEST001"
            )
            
            response = client.post('/', {
                'role': 'employee',
                'email': 'test@example.com',
                'password': 'password123'
            }, follow=True)
            
            print(f"   Login status: {response.status_code} - {'✅' if response.status_code == 200 else '❌'}")
            
            # Check if session was created
            if 'employee_id' in client.session:
                print(f"   Session created: ✅")
            else:
                print(f"   Session created: ❌")
                
            # Test logout
            print("\n5. Testing logout...")
            response = client.get('/logout/')
            print(f"   Logout status: {response.status_code} - {'✅' if response.status_code == 302 else '❌'}")
            
            # Check session after logout
            if 'employee_id' not in client.session:
                print(f"   Session cleared: ✅")
            else:
                print(f"   Session cleared: ❌")
            
            # Cleanup
            test_emp.delete()
            
        except Exception as e:
            print(f"   Test user creation failed: {e}")
        
        print("\n" + "=" * 40)
        print("📊 SUMMARY: Check if tests passed (✅) or failed (❌)")
        
    except Exception as e:
        print(f"❌ Test failed with error: {e}")

if __name__ == "__main__":
    test_simple_auth()