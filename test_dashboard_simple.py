#!/usr/bin/env python
"""
Test script to verify employee dashboard data fetching
"""
import os
import sys
import django

# Setup Django
sys.path.append('E:/Backend Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.utils import timezone
from django.db.models import Q
from app.models import Employee, Attendance, LeaveApply, Announcement

def test_database_data():
    """Test database data availability"""
    print("Testing Employee Dashboard Data Fetching...")
    
    # Check if there are any employees in the database
    employees = Employee.objects.all()
    print(f"Total employees in database: {employees.count()}")
    
    if employees.count() == 0:
        print("No employees found. Creating test employee...")
        # Create a test employee
        test_employee = Employee.objects.create(
            first_name="Test",
            last_name="Employee",
            email="test@employee.com",
            password="password123",
            company_id="EMP001",
            designation="Software Developer",
            department="IT",
            package=50000.00
        )
        print(f"Created test employee: {test_employee}")
    
    # Get first employee
    employee = Employee.objects.first()
    print(f"Testing with employee: {employee.first_name} {employee.last_name}")
    
    # Test attendance data
    print("\n--- ATTENDANCE DATA ---")
    attendance_records = Attendance.objects.filter(employee=employee)
    print(f"Total attendance records: {attendance_records.count()}")
    
    # Check today's attendance
    today = timezone.now().date()
    today_attendance = Attendance.objects.filter(employee=employee, attendance_date=today)
    print(f"Today's attendance records: {today_attendance.count()}")
    
    # Check current month attendance
    current_month = timezone.now().replace(day=1)
    month_attendance = Attendance.objects.filter(
        employee=employee,
        attendance_date__gte=current_month
    )
    print(f"Current month attendance records: {month_attendance.count()}")
    
    # Calculate present days
    present_days = month_attendance.filter(status__in=['present', 'late']).count()
    half_days = month_attendance.filter(status='half_day').count()
    print(f"Present days (including late): {present_days}")
    print(f"Half days: {half_days}")
    
    # Test leave data
    print("\n--- LEAVE DATA ---")
    leave_applications = LeaveApply.objects.filter(employee=employee)
    print(f"Total leave applications: {leave_applications.count()}")
    
    pending_leaves = LeaveApply.objects.filter(employee=employee, status='pending')
    print(f"Pending leave applications: {pending_leaves.count()}")
    
    # Test announcements
    print("\n--- ANNOUNCEMENTS ---")
    announcements = Announcement.objects.filter(status='published')
    print(f"Published announcements: {announcements.count()}")
    
    # Check active announcements (not expired)
    active_announcements = announcements.filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gte=timezone.now().date())
    )
    print(f"Active announcements: {active_announcements.count()}")
    
    # Test dashboard calculations
    print("\n--- DASHBOARD CALCULATIONS ---")
    
    # Calculate working days this month
    year = timezone.now().year
    month = timezone.now().month
    from calendar import monthrange
    _, num_days = monthrange(year, month)
    
    working_days = 0
    for day in range(1, num_days + 1):
        date_obj = timezone.now().replace(year=year, month=month, day=day)
        if date_obj.weekday() < 6:  # Monday to Saturday (0-5)
            working_days += 1
    
    print(f"Working days this month: {working_days}")
    
    # Calculate attendance rate
    total_present = present_days + half_days
    if working_days > 0:
        attendance_rate = round((total_present / working_days) * 100, 1)
    else:
        attendance_rate = 0.0
    
    print(f"Attendance rate: {attendance_rate}%")
    
    # Test leave statistics
    next_month = (current_month.replace(day=28) + timezone.timedelta(days=4)).replace(day=1)
    monthly_leaves = LeaveApply.objects.filter(
        employee=employee,
        start_date__gte=current_month,
        start_date__lt=next_month,
        status__in=['approved', 'pending']
    )
    
    leaves_used = sum([leave.total_days for leave in monthly_leaves])
    max_leaves = 10
    remaining_leaves = max(0, max_leaves - leaves_used)
    
    print(f"Leaves used this month: {leaves_used}")
    print(f"Remaining leaves: {remaining_leaves}")
    
    return {
        'employee': employee,
        'working_days': working_days,
        'present_days': present_days,
        'half_days': half_days,
        'attendance_rate': attendance_rate,
        'pending_leaves': pending_leaves.count(),
        'leaves_used': leaves_used,
        'remaining_leaves': remaining_leaves,
        'recent_attendance': attendance_records.order_by('-attendance_date')[:5],
        'recent_leaves': leave_applications.order_by('-applied_at')[:5],
        'announcements': active_announcements.order_by('-created_at')[:5]
    }

if __name__ == "__main__":
    print("Starting Dashboard Data Test\n")
    
    result = test_database_data()
    
    print("\n=== TEST SUMMARY ===")
    print(f"Employee: {result['employee'].first_name} {result['employee'].last_name}")
    print(f"Working Days: {result['working_days']}")
    print(f"Present Days: {result['present_days']}")
    print(f"Half Days: {result['half_days']}")
    print(f"Attendance Rate: {result['attendance_rate']}%")
    print(f"Pending Leaves: {result['pending_leaves']}")
    print(f"Leaves Used: {result['leaves_used']}")
    print(f"Remaining Leaves: {result['remaining_leaves']}")
    
    print("\nDashboard data testing completed successfully!")