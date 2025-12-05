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
from app.models import Employee, Attendance, LeaveApply, Announcement
from app.views import employee_dashboard

def test_dashboard_data():
    """Test dashboard data fetching"""
    print("🔍 Testing Employee Dashboard Data Fetching...")
    
    # Check if there are any employees in the database
    employees = Employee.objects.all()
    print(f"📊 Total employees in database: {employees.count()}")
    
    if employees.count() == 0:
        print("⚠️  No employees found. Creating test employee...")
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
        print(f"✅ Created test employee: {test_employee}")
    
    # Get first employee
    employee = Employee.objects.first()
    print(f"👤 Testing with employee: {employee.first_name} {employee.last_name}")
    
    # Create mock request object
    class MockRequest:
        def __init__(self, employee_id):
            self.session = {'employee_id': employee_id}
            self.method = 'GET'
            
    mock_request = MockRequest(employee.id)
    
    try:
        # Call dashboard view
        print("\n🔄 Calling employee_dashboard view...")
        response = employee_dashboard(mock_request)
        
        if response:
            print("✅ Dashboard view executed successfully")
            
            # Check context data
            if hasattr(response, 'context_data'):
                context = response.context_data
                print("\n📋 Dashboard Context Data:")
                print(f"  - Employee: {context.get('employee_obj', 'Not found')}")
                print(f"  - Working days: {context.get('working_days_this_month', 'Not found')}")
                print(f"  - Present days: {context.get('present_this_month', 'Not found')}")
                print(f"  - Attendance rate: {context.get('attendance_rate', 'Not found')}")
                print(f"  - Pending leaves: {context.get('pending_leaves', 'Not found')}")
                print(f"  - Recent attendance: {len(context.get('recent_attendance', []))} records")
                print(f"  - Recent leave applications: {len(context.get('recent_leave_applications', []))} records")
                print(f"  - Recent announcements: {len(context.get('recent_announcements', []))} records")
                
                # Check leave statistics
                leave_stats = context.get('leave_statistics', {})
                print(f"  - Leave stats: {leave_stats}")
                
            else:
                print("❌ Response doesn't have context_data")
        else:
            print("❌ Dashboard view returned None")
            
    except Exception as e:
        print(f"❌ Error calling dashboard: {str(e)}")
        import traceback
        traceback.print_exc()

def test_attendance_data():
    """Test attendance data"""
    print("\n🔍 Testing Attendance Data...")
    
    employees = Employee.objects.all()
    if employees.count() > 0:
        employee = employees.first()
        today = timezone.now().date()
        
        # Check attendance records
        attendance_records = Attendance.objects.filter(employee=employee)
        print(f"📅 Total attendance records for {employee.first_name}: {attendance_records.count()}")
        
        # Check today's attendance
        today_attendance = Attendance.objects.filter(employee=employee, attendance_date=today)
        print(f"📅 Today's attendance records: {today_attendance.count()}")
        
        # Check current month attendance
        current_month = timezone.now().replace(day=1)
        month_attendance = Attendance.objects.filter(
            employee=employee,
            attendance_date__gte=current_month
        )
        print(f"📅 Current month attendance records: {month_attendance.count()}")

def test_leave_data():
    """Test leave data"""
    print("\n🔍 Testing Leave Data...")
    
    employees = Employee.objects.all()
    if employees.count() > 0:
        employee = employees.first()
        
        # Check leave applications
        leave_applications = LeaveApply.objects.filter(employee=employee)
        print(f"📋 Total leave applications for {employee.first_name}: {leave_applications.count()}")
        
        # Check pending leaves
        pending_leaves = LeaveApply.objects.filter(employee=employee, status='pending')
        print(f"📋 Pending leave applications: {pending_leaves.count()}")

def test_announcements():
    """Test announcements"""
    print("\n🔍 Testing Announcements...")
    
    announcements = Announcement.objects.filter(status='published')
    print(f"📢 Published announcements: {announcements.count()}")
    
    # Check active announcements (not expired)
    active_announcements = announcements.filter(
        Q(expiry_date__isnull=True) | Q(expiry_date__gte=timezone.now().date())
    )
    print(f"📢 Active announcements: {active_announcements.count()}")

if __name__ == "__main__":
    print("🚀 Starting Dashboard Data Test\n")
    
    # Import Q for announcements query
    from django.db.models import Q
    
    test_dashboard_data()
    test_attendance_data()
    test_leave_data()
    test_announcements()
    
    print("\n✅ Dashboard data testing completed!")