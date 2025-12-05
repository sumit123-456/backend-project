#!/usr/bin/env python3
"""
Simple authentication test without unicode characters
"""

import os
import sys
import django

# Set up Django with correct settings module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

def test_authentication():
    """Test authentication requirements"""
    print("AUTHENTICATION TEST")
    print("=" * 40)
    
    from django.test import Client
    from app.models import Employee
    
    client = Client()
    
    # Test 1: Basic pages
    print("\n1. BASIC PAGE ACCESS")
    print("-" * 20)
    
    # Login page
    response = client.get('/')
    print(f"   Login page: {response.status_code} {'PASS' if response.status_code == 200 else 'FAIL'}")
    
    # Protected page
    response = client.get('/employee-dashboard/')
    print(f"   Protected page: {response.status_code} {'REDIRECT' if response.status_code == 302 else 'FAIL'}")
    
    # Attendance table
    response = client.get('/attendance-table/')
    print(f"   Attendance table: {response.status_code} {'PASS' if response.status_code == 200 else 'FAIL'}")
    
    # Test 2: Login/Logout cycle
    print("\n2. LOGIN/LOGOUT CYCLE")
    print("-" * 20)
    
    try:
        # Create test user
        test_emp = Employee.objects.create(
            first_name="Test", last_name="User",
            email="test@example.com", password="test123",
            company_id="TEST001"
        )
        
        # Login
        response = client.post('/', {
            'role': 'employee',
            'email': 'test@example.com',
            'password': 'test123'
        }, follow=True)
        
        login_ok = response.status_code == 200 and 'employee_id' in client.session
        print(f"   Login: {'PASS' if login_ok else 'FAIL'}")
        
        if login_ok:
            # Page access after login
            response = client.get('/employee-dashboard/')
            access_ok = response.status_code == 200
            print(f"   Page access: {'PASS' if access_ok else 'FAIL'}")
            
            # Logout
            response = client.get('/logout/')
            logout_ok = response.status_code == 302 and 'employee_id' not in client.session
            print(f"   Logout: {'PASS' if logout_ok else 'FAIL'}")
            
            if logout_ok:
                # Blocked access after logout
                response = client.get('/employee-dashboard/')
                blocked_ok = response.status_code == 302
                print(f"   Post-logout block: {'PASS' if blocked_ok else 'FAIL'}")
        
        # Cleanup
        test_emp.delete()
        
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n" + "=" * 40)
    print("SUMMARY: All tests should show PASS")

if __name__ == "__main__":
    test_authentication()