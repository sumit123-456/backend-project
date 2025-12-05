#!/usr/bin/env python3
"""
Test script to verify the 6:30 PM auto checkout functionality
"""

import os
import sys
import django
from datetime import datetime, time, date
from unittest.mock import patch, MagicMock

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import TestCase, Client
from app.models import Employee, Attendance, AttendanceCheckLog
from django.utils import timezone

def test_auto_checkout_functionality():
    """Test the 6:30 PM auto checkout functionality"""
    
    print("Testing Auto Checkout Functionality...")
    print("=" * 50)
    
    # Create a test employee
    test_employee = Employee.objects.create(
        first_name="Test",
        last_name="Employee", 
        email="testemployee@example.com",
        password="test123",
        company_id="TEST001",
        designation="Software Developer",
        department="IT",
        package=50000.00,
        address="Test Address"
    )
    
    print(f"Created test employee: {test_employee.first_name} {test_employee.last_name}")
    
    # Create a test attendance record for today with check-in
    today = timezone.now().date()
    test_attendance = Attendance.objects.create(
        employee=test_employee,
        attendance_date=today,
        check_in_time=time(10, 30),  # Checked in at 10:30 AM
        status="present",
        shift_type="full_time",
        is_check_in_allowed=False,
        can_check_out=False,
        remarks="Checked in at 10:30 AM"
    )
    
    print(f"Created test attendance record for {today}")
    
    # Test Case 1: At 6:30 PM (should auto checkout)
    print("\nTest Case: At 6:30 PM (Auto checkout should trigger)")
    
    # Mock the current time to be 6:30 PM
    with patch('app.views.timezone.now') as mock_now:
        mock_now.return_value = timezone.make_aware(datetime.combine(today, time(18, 30)))
        
        # Create a client and simulate login
        client = Client()
        session = client.session
        session['employee_id'] = test_employee.id
        session['role'] = 'employee'
        session['employee_name'] = f"{test_employee.first_name} {test_employee.last_name}"
        session.save()
        
        # Call the attendance view
        response = client.get('/employee/attendance/')
        
        # Refresh the attendance record to see if it was updated
        test_attendance.refresh_from_db()
        
        # Verify auto checkout happened
        assert test_attendance.check_out_time is not None, "Check-out time should be set"
        assert test_attendance.check_out_time == time(18, 30), "Check-out time should be 18:30"
        assert "Auto checkout at 6:30 PM" in test_attendance.remarks, "Remarks should contain auto checkout message"
        assert test_attendance.total_worked_hours >= 8.0, "Should have at least 8 hours worked"
        
        print("   Auto checkout correctly triggered at 6:30 PM")
        print(f"   Check-out time: {test_attendance.check_out_time}")
        print(f"   Worked hours: {test_attendance.total_worked_hours}")
        print(f"   Status: {test_attendance.status}")
        print(f"   Remarks: {test_attendance.remarks}")
        
        # Verify log entry was created
        auto_log = AttendanceCheckLog.objects.filter(
            employee=test_employee,
            check_type='check_out',
            check_time__date=today
        ).first()
        
        assert auto_log is not None, "Auto check-out log should be created"
        print("   Auto check-out log entry created successfully")
    
    # Test Case 2: Before 6:30 PM (should not auto checkout)
    print("\nTest Case: Before 6:30 PM (Auto checkout should NOT trigger)")
    
    # Create another test employee for this case
    test_employee2 = Employee.objects.create(
        first_name="Test2",
        last_name="Employee2", 
        email="testemployee2@example.com",
        password="test123",
        company_id="TEST002",
        designation="Software Developer",
        department="IT",
        package=50000.00,
        address="Test Address"
    )
    
    test_attendance2 = Attendance.objects.create(
        employee=test_employee2,
        attendance_date=today,
        check_in_time=time(10, 30),
        status="present",
        shift_type="full_time",
        is_check_in_allowed=False,
        can_check_out=False,
        remarks="Checked in at 10:30 AM"
    )
    
    with patch('app.views.timezone.now') as mock_now:
        mock_now.return_value = timezone.make_aware(datetime.combine(today, time(17, 45)))
        
        # Create a client and simulate login
        client2 = Client()
        session2 = client2.session
        session2['employee_id'] = test_employee2.id
        session2['role'] = 'employee'
        session2['employee_name'] = f"{test_employee2.first_name} {test_employee2.last_name}"
        session2.save()
        
        # Call the attendance view
        response2 = client2.get('/employee/attendance/')
        
        # Refresh the attendance record to see if it was updated
        test_attendance2.refresh_from_db()
        
        # Verify auto checkout did NOT happen
        assert test_attendance2.check_out_time is None, "Check-out time should still be None"
        assert "Auto checkout" not in test_attendance2.remarks, "Remarks should not contain auto checkout message"
        
        print("   Auto checkout correctly NOT triggered at 5:45 PM")
        print(f"   Check-out time: {test_attendance2.check_out_time}")
        print(f"   Remarks: {test_attendance2.remarks}")
    
    print("\nAll tests passed!")
    print("=" * 50)
    print("Auto Checkout Functionality Summary:")
    print("   • Time constant: 6:30 PM (18:30)")
    print("   • Triggers automatically when time >= 6:30 PM")
    print("   • Only triggers if employee has checked in")
    print("   • Only triggers if employee hasn't already checked out")
    print("   • Saves check-out time and calculates worked hours")
    print("   • Updates attendance status appropriately")
    print("   • Logs the auto check-out action")
    print("   • Displays 3-second success message in UI")
    
    # Cleanup
    test_employee.delete()
    test_employee2.delete()
    print("\nTest cleanup completed")

if __name__ == "__main__":
    test_auto_checkout_functionality()