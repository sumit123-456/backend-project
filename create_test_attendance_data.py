#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('e:/Backend Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from app.models import HRProfile, Employee, PresentRecord, AbsentRecord, LateMarkRecord, DailyWorkCompletion
from datetime import date, datetime, time, timedelta

def create_test_attendance_data():
    print("=== Creating Test Attendance Data ===")
    
    # Get existing data
    employees = Employee.objects.filter(resigned_date__isnull=True)
    hr = HRProfile.objects.first()
    
    if not employees.exists():
        print("No active employees found!")
        return False
    
    if not hr:
        print("No HR profile found!")
        return False
    
    print(f"Found {employees.count()} employees and {hr.full_name} as HR")
    
    today = date.today()
    yesterday = today - timedelta(days=1)
    
    created_records = 0
    
    # Create some test attendance records
    for i, employee in enumerate(employees):
        print(f"\n--- Creating records for {employee.first_name} {employee.last_name} ---")
        
        # Create PresentRecord for today
        present_record = PresentRecord.objects.create(
            employee=employee,
            attendance_date=today,
            marked_time=datetime.now(),
            check_in_time=time(9, 30),
            marked_by='self'
        )
        print(f"Created PresentRecord for {employee.first_name} - {today}")
        created_records += 1
        
        # Create LateMarkRecord for yesterday
        late_record = LateMarkRecord.objects.create(
            employee=employee,
            attendance_date=yesterday,
            marked_time=datetime.now(),
            actual_check_in_time=time(11, 15),
            late_minutes=90,  # 1.5 hours late
            marked_by='self'
        )
        print(f"Created LateMarkRecord for {employee.first_name} - {yesterday} (90 min late)")
        created_records += 1
        
        # Create AbsentRecord for 2 days ago
        absent_date = today - timedelta(days=2)
        absent_record = AbsentRecord.objects.create(
            employee=employee,
            attendance_date=absent_date,
            marked_time=datetime.now(),
            reason="Medical emergency - was sick",
            marked_by='self'
        )
        print(f"Created AbsentRecord for {employee.first_name} - {absent_date}")
        created_records += 1
        
        # Create WorkCompletion for today
        work_completion = DailyWorkCompletion.objects.create(
            employee=employee,
            work_date=today,
            tasks_completed="Completed module development, reviewed code, attended team meeting",
            challenges_faced="Faced some issues with database connection but resolved them",
            tomorrow_plan="Continue with testing and documentation",
            additional_notes="Productive day overall",
            work_completion_time=datetime.now(),
            status='completed'
        )
        print(f"Created DailyWorkCompletion for {employee.first_name} - {today}")
        created_records += 1
    
    print(f"\n=== Test Data Creation Summary ===")
    print(f"Total records created: {created_records}")
    print(f"Present Records: {PresentRecord.objects.count()}")
    print(f"Absent Records: {AbsentRecord.objects.count()}")
    print(f"Late Mark Records: {LateMarkRecord.objects.count()}")
    print(f"Work Completions: {DailyWorkCompletion.objects.count()}")
    
    return True

if __name__ == "__main__":
    create_test_attendance_data()