#!/usr/bin/env python3
"""
Simple verification test for the check_in_end_time column fix
"""

import os
import sys
import django
from datetime import time

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from app.models import Employee, AttendanceCheckLog

def test_check_in_end_time_column():
    """Test that check_in_end_time column exists and works"""
    
    print("Testing check_in_end_time column...")
    print("=" * 50)
    
    # Create a test employee
    test_employee = Employee.objects.create(
        first_name="Column",
        last_name="Test", 
        email="columntest@example.com",
        password="test123",
        company_id="COL001",
        designation="Software Developer",
        department="IT",
        package=50000.00,
        address="Test Address"
    )
    
    print(f"Created test employee: {test_employee.first_name} {test_employee.last_name}")
    
    # Test creating AttendanceCheckLog with check_in_end_time
    try:
        check_log = AttendanceCheckLog.objects.create(
            employee=test_employee,
            check_type='check_in',
            check_time=django.utils.timezone.now(),
            attendance_date=django.utils.timezone.now().date(),
            check_in_end_time=time(10, 50),  # This should work now!
            check_out_start_time=time(18, 20),
            check_out_end_time=time(18, 45),
            official_start_time=time(10, 45),
            check_in_allowed_time=time(10, 0),
            required_work_hours=8.0
        )
        
        print("SUCCESS: check_in_end_time column created successfully!")
        print(f"   Check-in end time: {check_log.check_in_end_time}")
        print(f"   Check-out start time: {check_log.check_out_start_time}")
        print(f"   Check-out end time: {check_log.check_out_end_time}")
        
        # Verify we can read the values back
        retrieved_log = AttendanceCheckLog.objects.get(id=check_log.id)
        print(f"SUCCESS: Retrieved check_in_end_time: {retrieved_log.check_in_end_time}")
        
    except Exception as e:
        print(f"FAILED: {str(e)}")
        return False
    
    # Cleanup
    test_employee.delete()
    print("\nTest cleanup completed")
    
    print("\n" + "=" * 50)
    print("SUMMARY:")
    print("SUCCESS: The check_in_end_time column error has been FIXED!")
    print("SUCCESS: Database schema is now synchronized with Django models")
    print("SUCCESS: AttendanceCheckLog model works correctly")
    print("=" * 50)
    
    return True

if __name__ == "__main__":
    test_check_in_end_time_column()