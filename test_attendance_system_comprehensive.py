#!/usr/bin/env python
"""
Comprehensive Attendance System Test Script
Tests all components of the attendance system across all modules
"""

import os
import sys
import django
from datetime import date, time, datetime, timedelta

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.utils import timezone
from django.db.models import Count
from app.models import (
    Employee, Attendance, TeamLeader, TeamAssignment, HRProfile, 
    LeaveApply, MonthlyAttendanceSummary, AttendanceApproval, 
    AttendanceCheckLog, PayrollDeduction, SalaryProcessing
)

def test_database_connection():
    """Test database connectivity and basic model counts"""
    print("🔍 DATABASE CONNECTION TEST")
    print("-" * 50)
    
    try:
        # Test basic model imports and counts
        emp_count = Employee.objects.count()
        hr_count = HRProfile.objects.count()
        tl_count = TeamLeader.objects.count()
        att_count = Attendance.objects.count()
        
        print(f"✅ Database connection: OK")
        print(f"📊 Employees: {emp_count}")
        print(f"👔 HR Profiles: {hr_count}")
        print(f"👥 Team Leaders: {tl_count}")
        print(f"📅 Attendance Records: {att_count}")
        print(f"📋 Leave Applications: {LeaveApply.objects.count()}")
        print(f"📊 Monthly Summaries: {MonthlyAttendanceSummary.objects.count()}")
        print(f"⚖️ Attendance Approvals: {AttendanceApproval.objects.count()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database error: {str(e)}")
        return False

def test_model_relationships():
    """Test model relationships and data integrity"""
    print("\n🔗 MODEL RELATIONSHIPS TEST")
    print("-" * 50)
    
    try:
        # Check Employee-Attendance relationship
        if Employee.objects.exists():
            sample_employee = Employee.objects.first()
            employee_attendance_count = Attendance.objects.filter(employee=sample_employee).count()
            print(f"✅ Employee-Attendance: {sample_employee.first_name} has {employee_attendance_count} attendance records")
        
        # Check Team Assignment relationships
        if TeamLeader.objects.exists():
            sample_tl = TeamLeader.objects.first()
            team_size = TeamAssignment.objects.filter(team_leader=sample_tl).count()
            print(f"✅ Team Leader assignments: TL has {team_size} team members")
            
        # Check HR relationships
        if HRProfile.objects.exists():
            sample_hr = HRProfile.objects.first()
            print(f"✅ HR Profile: {sample_hr.full_name} ({sample_hr.employee_id})")
        
        return True
        
    except Exception as e:
        print(f"❌ Relationship error: {str(e)}")
        return False

def test_attendance_records():
    """Test attendance records and functionality"""
    print("\n📅 ATTENDANCE RECORDS TEST")
    print("-" * 50)
    
    try:
        today = timezone.now().date()
        today_attendance = Attendance.objects.filter(attendance_date=today)
        
        print(f"📅 Today ({today}): {today_attendance.count()} records")
        
        # Check different attendance statuses
        statuses = ['present', 'absent', 'half_day', 'late', 'leave', 'holiday', 'weekend']
        for status in statuses:
            count = today_attendance.filter(status=status).count()
            if count > 0:
                print(f"📋 Status '{status}': {count} records")
        
        # Check recent attendance (last 7 days)
        week_ago = today - timedelta(days=7)
        week_attendance = Attendance.objects.filter(attendance_date__gte=week_ago)
        print(f"📆 Last 7 days: {week_attendance.count()} total records")
        
        # Check for missing check-in/check-out times
        missing_checkin = Attendance.objects.filter(check_in_time__isnull=True, attendance_date=today).count()
        missing_checkout = Attendance.objects.filter(
            check_in_time__isnull=False, 
            check_out_time__isnull=True, 
            attendance_date=today
        ).count()
        
        print(f"⏰ Missing check-in today: {missing_checkin}")
        print(f"⏰ Missing check-out today: {missing_checkout}")
        
        # Check for records with approval status
        approved_records = Attendance.objects.filter(
            approval__status='approved'
        ).count()
        pending_records = Attendance.objects.filter(
            approval__status='pending'
        ).count()
        
        print(f"✅ Approved records: {approved_records}")
        print(f"⏳ Pending approvals: {pending_records}")
        
        return True
        
    except Exception as e:
        print(f"❌ Attendance check error: {str(e)}")
        return False

def main():
    """Main test function"""
    print("🚀 STARTING COMPREHENSIVE ATTENDANCE SYSTEM TEST")
    print("=" * 70)
    
    # Run all tests
    results = []
    
    results.append(test_database_connection())
    results.append(test_model_relationships())
    results.append(test_attendance_records())
    
    # Generate summary
    print("\n" + "=" * 70)
    print("📊 COMPREHENSIVE ATTENDANCE SYSTEM TEST SUMMARY")
    print("=" * 70)
    
    total_tests = len(results)
    passed_tests = sum(1 for result in results if result)
    failed_tests = total_tests - passed_tests
    
    print(f"\n📈 TEST RESULTS:")
    print(f"   Total Tests: {total_tests}")
    print(f"   ✅ Passed: {passed_tests}")
    print(f"   ❌ Failed: {failed_tests}")
    print(f"   📊 Success Rate: {(passed_tests/total_tests)*100:.1f}%")

if __name__ == "__main__":
    main()