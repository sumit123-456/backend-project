#!/usr/bin/env python
"""
Quick System Health Check - Tests all critical modules
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import Client
from django.utils import timezone
from django.db.models import Count
from app.models import (
    Employee, HRProfile, TeamLeader, TeamAssignment, ProjectAssignment,
    Attendance, LeaveApply, LeaveApproval, Payroll, Announcement,
    PresentRecord, AbsentRecord, LateMarkRecord, DailyWorkCompletion
)

def quick_health_check():
    """Quick system health check"""
    print("HR SYSTEM HEALTH CHECK")
    print("=" * 60)
    
    issues = []
    successes = []
    client = Client()
    
    # 1. Database Test
    try:
        emp_count = Employee.objects.count()
        hr_count = HRProfile.objects.count()
        tl_count = TeamLeader.objects.count()
        attendance_count = Attendance.objects.count()
        
        successes.append(f"Database OK - {emp_count} employees, {hr_count} HR, {tl_count} TL")
        
        # Test relationships
        if Employee.objects.exists():
            sample_emp = Employee.objects.first()
            team_assignments = TeamAssignment.objects.filter(employee=sample_emp).count()
            successes.append(f"Employee-TL relationships working ({team_assignments} assignments)")
            
    except Exception as e:
        issues.append(f"Database Error: {str(e)}")
    
    # 2. URL Accessibility Test
    public_urls = [('/', 'Login'), ('/create-hr/', 'Create HR'), ('/hr-list/', 'HR List')]
    for url, desc in public_urls:
        try:
            response = client.get(url)
            if response.status_code == 200:
                successes.append(f"{desc} page accessible")
            else:
                issues.append(f"{desc} page returned {response.status_code}")
        except Exception as e:
            issues.append(f"{desc} page error: {str(e)}")
    
    # 3. Enhanced Attendance Test
    try:
        present_records = PresentRecord.objects.count()
        absent_records = AbsentRecord.objects.count()
        late_mark_records = LateMarkRecord.objects.count()
        
        if present_records > 0 or absent_records > 0 or late_mark_records > 0:
            successes.append(f"Enhanced attendance working ({present_records} present, {absent_records} absent, {late_mark_records} late)")
        else:
            issues.append("No enhanced attendance records found")
            
    except Exception as e:
        issues.append(f"Enhanced attendance error: {str(e)}")
    
    # 4. Leave System Test
    try:
        leave_applications = LeaveApply.objects.count()
        pending_leaves = LeaveApply.objects.filter(status='pending').count()
        approved_leaves = LeaveApply.objects.filter(status='approved').count()
        
        successes.append(f"Leave system OK - {leave_applications} applications ({pending_leaves} pending, {approved_leaves} approved)")
        
        # Check templates
        from django.template.loader import get_template
        try:
            get_template('app/employee/leave-apply.html')
            successes.append("Leave apply template exists")
        except:
            issues.append("Leave apply template missing")
            
        try:
            get_template('app/hr/leave-approval.html')
            successes.append("HR leave approval template exists")
        except:
            issues.append("HR leave approval template missing")
            
    except Exception as e:
        issues.append(f"Leave system error: {str(e)}")
    
    # 5. Payroll Test
    try:
        payroll_records = Payroll.objects.count()
        processed_payroll = Payroll.objects.filter(is_processed=True).count()
        
        if payroll_records > 0:
            successes.append(f"Payroll system OK - {payroll_records} records ({processed_payroll} processed)")
        else:
            issues.append("No payroll records found")
            
    except Exception as e:
        issues.append(f"Payroll system error: {str(e)}")
    
    # 6. Template Test
    try:
        from django.template.loader import get_template
        
        critical_templates = [
            ('app/base.html', 'Base template'),
            ('app/login.html', 'Login template'),
            ('app/hr/dashboard.html', 'HR Dashboard'),
            ('app/employee/dashboard.html', 'Employee Dashboard'),
            ('app/tl/dashboard.html', 'TL Dashboard'),
        ]
        
        for template_path, desc in critical_templates:
            try:
                template = get_template(template_path)
                successes.append(f"{desc} template accessible")
            except Exception as e:
                issues.append(f"{desc} template error: {str(e)}")
                
    except Exception as e:
        issues.append(f"Template system error: {str(e)}")
    
    # 7. Team Management Test
    try:
        team_assignments = TeamAssignment.objects.count()
        project_assignments = ProjectAssignment.objects.count()
        
        if team_assignments > 0:
            successes.append(f"Team management OK - {team_assignments} team assignments")
        else:
            issues.append("No team assignments found")
            
        if project_assignments > 0:
            successes.append(f"Project management OK - {project_assignments} project assignments")
        else:
            issues.append("No project assignments found")
            
    except Exception as e:
        issues.append(f"Team management error: {str(e)}")
    
    # 8. Announcements Test
    try:
        announcements = Announcement.objects.count()
        published_announcements = Announcement.objects.filter(status='published').count()
        
        if announcements > 0:
            successes.append(f"Announcements OK - {announcements} total ({published_announcements} published)")
        else:
            issues.append("No announcements found")
            
    except Exception as e:
        issues.append(f"Announcements error: {str(e)}")
    
    # Results
    print(f"\nSUCCESSES ({len(successes)}):")
    for success in successes:
        print(f"   + {success}")
    
    print(f"\nISSUES ({len(issues)}):")
    for issue in issues:
        print(f"   - {issue}")
    
    total = len(successes) + len(issues)
    success_rate = (len(successes) / total * 100) if total > 0 else 0
    
    print(f"\nSUMMARY:")
    print(f"   Total Checks: {total}")
    print(f"   Success Rate: {success_rate:.1f}%")
    
    if len(issues) == 0:
        print(f"\nSYSTEM HEALTH: EXCELLENT - No issues found!")
    elif len(issues) <= 3:
        print(f"\nSYSTEM HEALTH: GOOD - Few minor issues")
    else:
        print(f"\nSYSTEM HEALTH: NEEDS ATTENTION - Multiple issues found")

if __name__ == "__main__":
    quick_health_check()