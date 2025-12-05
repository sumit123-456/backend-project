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

def test_employee_payslip():
    """Test employee payslip view by simulating login"""
    client = Client()
    
    # Get the test employee by company_id instead of email
    try:
        employee = Employee.objects.get(company_id='EMP001')
        print(f"Found test employee: {employee.first_name} {employee.last_name}")
        print(f"Employee ID: {employee.id}")
        print(f"Company ID: {employee.company_id}")
        print(f"Email: {employee.email}")
        
        # Check if this employee has payroll records
        payroll_count = employee.payroll_set.count()
        print(f"Payroll records: {payroll_count}")
        
        if payroll_count > 0:
            print("\nPayroll Records:")
            for payroll in employee.payroll_set.all():
                print(f"  - {payroll.month} {payroll.year}: Rs.{payroll.final_salary} ({'Processed' if payroll.is_processed else 'Pending'})")
        
        # Test the payslip view by making a request with employee_id in session
        session = client.session
        session['employee_id'] = employee.id
        session.save()
        
        # Try the correct payslip URL
        response = client.get('/payslip/')
        print(f"Response status code: {response.status_code}")
        
        # If it's a redirect, try to bypass it and test the view directly
        if response.status_code == 302:
            # Let's test the view function directly
            print("Testing view function directly...")
            from app.views import employee_payslip
            from django.http import HttpRequest
            from django.contrib.sessions.middleware import SessionMiddleware
            
            # Create a request object
            request = HttpRequest()
            request.method = 'GET'
            request.session = session
            request.META['HTTP_HOST'] = 'localhost'
            
            try:
                response = employee_payslip(request)
                print(f"Direct view response status: {response.status_code}")
                
                if response.status_code == 200:
                    print("SUCCESS: Payslip view executed successfully!")
                    content = response.content.decode()
                    if "Payroll Records" in content:
                        print("SUCCESS: Payroll Records section found in template")
                    if "John Doe" in content:
                        print("SUCCESS: Employee name found in template")
                    if "Rs." in content:
                        print("SUCCESS: Indian Rupee formatting found in template")
                    if "November" in content:
                        print("SUCCESS: Payroll month data found in template")
                else:
                    print(f"ERROR: Direct view failed with status: {response.status_code}")
                    print("Response content:", content[:500])
                    
            except Exception as e:
                print(f"ERROR in direct view test: {str(e)}")
        else:
            print(f"ERROR: Unexpected response status: {response.status_code}")
            
    except Employee.DoesNotExist:
        print("ERROR: Test employee not found!")
        print("Available employees:")
        for emp in Employee.objects.all():
            print(f"  - {emp.first_name} {emp.last_name} ({emp.company_id})")

if __name__ == '__main__':
    test_employee_payslip()