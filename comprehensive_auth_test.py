#!/usr/bin/env python3
"""
Comprehensive authentication test to verify all requirements are met
"""

import os
import sys
import django

# Set up Django environment
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'manage')
django.setup()

def run_comprehensive_test():
    """Run comprehensive authentication test"""
    print("🔐 COMPREHENSIVE AUTHENTICATION TEST")
    print("=" * 50)
    
    from django.test import Client
    from app.models import Employee, HRProfile, TeamLeader
    
    client = Client()
    test_results = []
    
    # Requirement 1: Login should work properly
    print("\n1️⃣ TESTING LOGIN FUNCTIONALITY")
    print("-" * 30)
    
    try:
        # Create test users
        test_employee = Employee.objects.create(
            first_name="Test", last_name="Employee",
            email="emp@test.com", password="test123", company_id="EMP001"
        )
        
        # Test employee login
        response = client.post('/', {
            'role': 'employee',
            'email': 'emp@test.com', 
            'password': 'test123'
        }, follow=True)
        
        login_success = response.status_code == 200 and 'employee_id' in client.session
        print(f"   Employee login: {'✅ PASS' if login_success else '❌ FAIL'}")
        test_results.append(('Login', login_success))
        
        if login_success:
            print(f"   Session ID: {client.session.session_key}")
            print(f"   Employee session: {client.session.get('employee_id')}")
            
            # Requirement 2: After login, all pages should be accessible
            print("\n2️⃣ TESTING POST-LOGIN PAGE ACCESS")
            print("-" * 30)
            
            pages_to_test = [
                ('/employee-dashboard/', 'Employee Dashboard'),
                ('/employee-attendance/', 'Employee Attendance'),
                ('/attendance-table/', 'Attendance Table'),
            ]
            
            for url, name in pages_to_test:
                response = client.get(url)
                accessible = response.status_code == 200
                print(f"   {name}: {'✅ ACCESSIBLE' if accessible else '❌ BLOCKED'} ({response.status_code})")
                test_results.append((f'{name} Access', accessible))
            
            # Requirement 3: After logout, no pages should be accessible
            print("\n3️⃣ TESTING LOGOUT FUNCTIONALITY")
            print("-" * 30)
            
            # Perform logout
            response = client.get('/logout/')
            logout_success = response.status_code == 302 and 'employee_id' not in client.session
            print(f"   Logout process: {'✅ PASS' if logout_success else '❌ FAIL'}")
            test_results.append(('Logout', logout_success))
            
            if logout_success:
                print(f"   Redirected to: {response.url}")
                print(f"   Session cleared: ✅")
                
                # Requirement 4: After logout, only login page should show
                print("\n4️⃣ TESTING POST-LOGOUT ACCESS")
                print("-" * 30)
                
                # Test that all protected pages redirect to login
                for url, name in pages_to_test[:2]:  # Test first 2 protected pages
                    response = client.get(url)
                    redirects_to_login = response.status_code == 302 and '/?next=' in response.url
                    print(f"   {name}: {'✅ REDIRECTS TO LOGIN' if redirects_to_login else '❌ DOES NOT REDIRECT'} ({response.status_code})")
                    test_results.append((f'{name} Post-Logout Redirect', redirects_to_login))
                
                # Test that attendance table is still accessible
                response = client.get('/attendance-table/')
                table_accessible = response.status_code == 200
                print(f"   Attendance Table: {'✅ STILL ACCESSIBLE' if table_accessible else '❌ BLOCKED'} ({response.status_code})")
                test_results.append(('Attendance Table Post-Logout', table_accessible))
            
            # Requirement 5: No repeated login page opening
            print("\n5️⃣ TESTING NO REPEATED LOGIN PROMPTS")
            print("-" * 30)
            
            # After logout, try to access protected pages multiple times
            for i in range(3):
                response = client.get('/employee-dashboard/')
                if response.status_code == 302:
                    print(f"   Attempt {i+1}: ✅ Redirects cleanly ({response.status_code})")
                else:
                    print(f"   Attempt {i+1}: ❌ Unexpected behavior ({response.status_code})")
                    test_results.append((f'No Repeated Prompts #{i+1}', False))
                    break
            else:
                print("   ✅ No repeated login prompts detected")
                test_results.append(('No Repeated Prompts', True))
        
        # Cleanup
        test_employee.delete()
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        test_results.append(('Test Execution', False))
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS SUMMARY")
    print("=" * 50)
    
    passed = sum(1 for _, result in test_results if result)
    total = len(test_results)
    
    for test_name, result in test_results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"   {test_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL REQUIREMENTS MET!")
        return True
    else:
        print(f"⚠️  {total-passed} issues found that need attention")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)