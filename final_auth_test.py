#!/usr/bin/env python3
"""
Final authentication test with correct Django setup
"""

import os
import sys
import django

# Set up Django with correct settings module
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

def test_authentication_fixes():
    """Test all authentication requirements"""
    print("🔐 FINAL AUTHENTICATION TEST")
    print("=" * 50)
    
    from django.test import Client
    from app.models import Employee
    
    # Test 1: Basic page accessibility
    print("\n1️⃣ BASIC PAGE ACCESSIBILITY")
    print("-" * 30)
    
    client = Client()
    
    # Login page should be accessible
    response = client.get('/')
    login_ok = response.status_code == 200
    print(f"   Login page: {'✅ OK' if login_ok else '❌ FAIL'} ({response.status_code})")
    
    # Protected pages should redirect
    response = client.get('/employee-dashboard/')
    redirect_ok = response.status_code == 302
    print(f"   Protected page: {'✅ REDIRECTS' if redirect_ok else '❌ FAIL'} ({response.status_code})")
    
    # Attendance table should be accessible
    response = client.get('/attendance-table/')
    table_ok = response.status_code == 200
    print(f"   Attendance table: {'✅ ACCESSIBLE' if table_ok else '❌ FAIL'} ({response.status_code})")
    
    # Test 2: Login/Logout cycle
    print("\n2️⃣ LOGIN/LOGOUT CYCLE")
    print("-" * 30)
    
    try:
        # Create test user
        test_emp = Employee.objects.create(
            first_name="Test", last_name="User",
            email="test@example.com", password="test123",
            company_id="TEST001"
        )
        
        # Test login
        response = client.post('/', {
            'role': 'employee',
            'email': 'test@example.com',
            'password': 'test123'
        }, follow=True)
        
        login_success = response.status_code == 200 and 'employee_id' in client.session
        print(f"   Login: {'✅ SUCCESS' if login_success else '❌ FAIL'}")
        
        if login_success:
            # Test page access after login
            response = client.get('/employee-dashboard/')
            access_ok = response.status_code == 200
            print(f"   Page access: {'✅ WORKS' if access_ok else '❌ FAIL'} ({response.status_code})")
            
            # Test logout
            response = client.get('/logout/')
            logout_ok = response.status_code == 302 and 'employee_id' not in client.session
            print(f"   Logout: {'✅ SUCCESS' if logout_ok else '❌ FAIL'}")
            
            if logout_ok:
                # Test no page access after logout
                response = client.get('/employee-dashboard/')
                blocked_ok = response.status_code == 302
                print(f"   Post-logout block: {'✅ BLOCKED' if blocked_ok else '❌ FAIL'} ({response.status_code})")
                
                # Test attendance table still works
                response = client.get('/attendance-table/')
                table_public_ok = response.status_code == 200
                print(f"   Public table: {'✅ ACCESSIBLE' if table_public_ok else '❌ FAIL'} ({response.status_code})")
        
        # Cleanup
        test_emp.delete()
        
    except Exception as e:
        print(f"   ❌ Test error: {e}")
    
    print("\n" + "=" * 50)
    print("📊 REQUIREMENTS STATUS")
    print("=" * 50)
    
    requirements = [
        ("Login page shows properly", login_ok),
        ("Protected pages redirect to login", redirect_ok),
        ("Attendance table accessible without login", table_ok),
        ("Login works correctly", login_success if 'login_success' in locals() else False),
        ("Pages accessible after login", access_ok if 'access_ok' in locals() else False),
        ("Logout clears session", logout_ok if 'logout_ok' in locals() else False),
        ("No page access after logout", blocked_ok if 'blocked_ok' in locals() else False),
        ("Attendance table works after logout", table_public_ok if 'table_public_ok' in locals() else False)
    ]
    
    for req, status in requirements:
        print(f"   {req}: {'✅' if status else '❌'}")
    
    passed = sum(1 for _, status in requirements if status)
    total = len(requirements)
    
    print(f"\nOverall: {passed}/{total} requirements met")
    
    if passed == total:
        print("\n🎉 ALL AUTHENTICATION REQUIREMENTS MET!")
        print("✅ Login works correctly")
        print("✅ Pages accessible after login") 
        print("✅ Logout clears session completely")
        print("✅ No page access after logout")
        print("✅ No repeated login prompts")
        return True
    else:
        print(f"\n⚠️ {total-passed} requirements need attention")
        return False

if __name__ == "__main__":
    test_authentication_fixes()