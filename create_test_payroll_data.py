#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append('e:/Backend Project')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from app.models import Employee, Payroll
from django.utils import timezone
from decimal import Decimal

def create_test_data():
    # Get or create a test employee
    try:
        employee = Employee.objects.get(email='test.employee@example.com')
        print(f'Using existing employee: {employee.first_name} {employee.last_name}')
    except Employee.DoesNotExist:
        # Try to find employee by company_id first
        try:
            employee = Employee.objects.get(company_id='EMP001')
            print(f'Found employee by company_id: {employee.first_name} {employee.last_name}')
        except Employee.DoesNotExist:
            # Create new employee with a unique company_id
            employee = Employee.objects.create(
                email='test.employee@example.com',
                first_name='John',
                last_name='Doe',
                password='password123',
                company_id='EMP999',  # Unique ID
                designation='Software Developer',
                department='IT',
                package=50000.00,
                address='123 Main St, City'
            )
            print(f'Created new test employee: {employee.first_name} {employee.last_name}')

    # Create sample payroll records for the last 6 months
    months = ['November 2025', 'October 2025', 'September 2025', 'August 2025', 'July 2025', 'June 2025']
    years = [2025, 2025, 2025, 2025, 2025, 2025]

    for i, (month, year) in enumerate(zip(months, years)):
        # Create payroll record
        payroll, created = Payroll.objects.get_or_create(
            employee=employee,
            month=month,
            year=year,
            defaults={
                'base_salary': Decimal('45000.00'),
                'allowances': Decimal('5000.00'),
                'overtime_amount': Decimal('2000.00') if i % 2 == 0 else Decimal('0.00'),
                'leave_deduction': Decimal('1500.00') if i == 1 else Decimal('0.00'),
                'late_arrival_deduction': Decimal('500.00') if i == 2 else Decimal('0.00'),
                'half_day_deduction': Decimal('750.00') if i == 3 else Decimal('0.00'),
                'other_deductions': Decimal('200.00'),
                'pf_deduction': Decimal('5400.00'),
                'professional_tax': Decimal('200.00'),
                'gross_salary': Decimal('52000.00') if i % 2 == 0 else Decimal('50000.00'),
                'total_deductions': Decimal('7850.00') if i == 1 else Decimal('6300.00'),
                'final_salary': Decimal('44150.00') if i == 1 else Decimal('43700.00'),
                'created_by': 'Test HR Admin',
                'is_processed': True if i < 4 else False,
                'processed_date': timezone.now() if i < 4 else None
            }
        )
        
        if created:
            print(f'Created payroll record for {month} {year}')
        else:
            print(f'Payroll already exists for {month} {year}')

    print('Test data creation completed!')
    print(f'Total payroll records for {employee.first_name} {employee.last_name}: {Payroll.objects.filter(employee=employee).count()}')

if __name__ == '__main__':
    create_test_data()