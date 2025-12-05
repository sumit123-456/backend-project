#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:/Backend Project')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from app.models import Employee
from django.test import Client
from django.urls import reverse

def debug_payroll_issue():
    """Debug the payroll issue by testing the complete flow"""
    print("=== DEBUGGING PAYROLL ISSUE ===")
    print()
    
    client = Client()
    
    # Step 1: Check if test employee exists
    try:
        employee = Employee.objects.get(company_id='EMP001')
        print(f"Test employee found: {employee.first_name} {employee.last_name} (ID: {employee.id})")
        print(f"Email: {employee.email}")
        
        # Step 2: Test accessing payslip without login
        print()
        print("1. Testing payslip access WITHOUT login:")
        response = client.get('/payslip/')
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 302:
            print(f"   Redirect URL: {response.url}")
            print("   EXPECTED: Redirects to login (user not authenticated)")
        
        # Step 3: Test login process
        print()
        print("2. Testing employee login process:")
        login_data = {
            'role': 'employee',
            'email': employee.email,
            'password': employee.password
        }
        response = client.post('/', login_data, follow=True)
        print(f"   Login Status: {response.status_code}")
        
        # Check if session has employee_id
        session = client.session
        if 'employee_id' in session:
            print(f"   Session employee_id: {session['employee_id']}")
        else:
            print("   No employee_id in session")
            return
        
        # Step 4: Test payslip access WITH login
        print()
        print("3. Testing payslip access WITH login:")
        response = client.get('/payslip/')
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   SUCCESS: Payslip page loads correctly!")
            content = response.content.decode()
            if "My Payroll" in content:
                print("   SUCCESS: 'My Payroll' title found")
            if "Payroll Records" in content:
                print("   SUCCESS: Payroll Records section found")
        elif response.status_code == 302:
            print(f"   STILL REDIRECTING to: {response.url}")
            print("   This indicates session/authentication issue")
        else:
            print(f"   ERROR: Unexpected status code {response.status_code}")
        
        # Step 5: Test URL generation
        print()
        print("4. Testing URL generation:")
        payslip_url = reverse('payslip')
        print(f"   Generated URL: {payslip_url}")
        print(f"   Expected URL: /payslip/")
        
        if payslip_url == '/payslip/':
            print("   URL generation is correct")
        else:
            print("   URL generation issue")
            
    except Employee.DoesNotExist:
        print("Test employee not found!")
        print("Available employees:")
        for emp in Employee.objects.all():
            print(f"  - {emp.first_name} {emp.last_name} ({emp.company_id})")
    
    print()
    print("=== SUMMARY ===")
    print("If the payslip page doesn't open when clicking the payroll link:")
    print("1. User must be logged in as an employee")
    print("2. Session must contain employee_id")
    print("3. Employee must have payroll records (or see empty state)")
    print("4. No JavaScript errors should prevent navigation")

if __name__ == '__main__':
    debug_payroll_issue()