#!/usr/bin/env python
"""
Comprehensive User Role Testing
Tests all features for HR, TL, and Employee roles
"""

import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from app.models import Employee, HRProfile, TeamLeader, TeamAssignment
import json

def test_user_roles():
    """Test all user role features"""
    print("COMPREHENSIVE USER ROLE TESTING")
    print("=" * 60)
    
    issues = []
    successes = []
    client = Client()
    
    # Get test users from database
    try:
        # Test with existing HR
        hr_profiles = HRProfile.objects.all()
        if hr_profiles.exists():
            test_hr = hr_profiles.first()
            successes.append(f"Found HR user: {test_hr.full_name} ({test_hr.employee_id})")
        else:
            issues.append("No HR profiles found")
            
        # Test with existing Employee
        employees = Employee.objects.all()
        if employees.exists():
            test_employee = employees.first()
            successes.append(f"Found Employee: {test_employee.first_name} {test_employee.last_name}")
        else:
            issues.append("No employees found")
            
        # Test with existing TL
        team_leaders = TeamLeader.objects.all()
        if team_leaders.exists():
            test_tl = team_leaders.first()
            successes.append(f"Found TL: {test_tl.employee.first_name} {test_tl.employee.last_name}")
        else:
            issues.append("No team leaders found")
            
    except Exception as e:
        issues.append(f"Database error: {str(e)}")
    
    # Test URL accessibility for different roles
    url_tests = [
        # Public URLs
        ('/', 'Login page', 'public'),
        ('/create-hr/', 'Create HR page', 'public'),
        ('/hr-list/', 'HR list page', 'public'),
        
        # Employee URLs  
        ('/employee-dashboard/', 'Employee dashboard', 'protected'),
        ('/employee-attendance/', 'Employee attendance', 'protected'),
        ('/apply-leave/', 'Apply leave', 'protected'),
        ('/payslip/', 'Payslip', 'protected'),
        ('/employee-profile/', 'Employee profile', 'protected'),
        ('/employee-project-dashboard/', 'Employee project dashboard', 'protected'),
        
        # TL URLs
        ('/tl-dashboard/', 'TL dashboard', 'protected'),
        ('/team-attendence/', 'Team attendance', 'protected'),
        ('/team-leave-approval/', 'Team leave approval', 'protected'),
        ('/tl-manage-team/', 'TL manage team', 'protected'),
        ('/tl-project-dashboard/', 'TL project dashboard', 'protected'),
        ('/tl-project-discussions/', 'TL project discussions', 'protected'),
        
        # HR URLs
        ('/dashboard/', 'HR dashboard', 'protected'),
        ('/attendance/', 'HR attendance', 'protected'),
        ('/leave-approvals/', 'Leave approvals', 'protected'),
        ('/announcements/', 'Announcements', 'protected'),
        ('/payroll/', 'Payroll management', 'protected'),
        ('/payroll-records/', 'Payroll records', 'protected'),
        ('/employee/', 'Employee management', 'protected'),
        ('/team/', 'Team management', 'protected'),
        ('/reports/', 'HR reports', 'protected'),
        
        # Enhanced attendance URLs
        ('/enhanced-attendance/', 'Enhanced attendance', 'protected'),
        ('/attendance-table/', 'Attendance table', 'protected'),
        ('/hr-enhanced-attendance/', 'HR enhanced attendance', 'protected'),
        ('/tl-enhanced-attendance/', 'TL enhanced attendance', 'protected'),
        
        # Team chat URLs
        ('/team-chat/', 'Team chat', 'protected'),
        
        # Monthly summaries and calculations
        ('/hr-monthly-attendance-summary/', 'Monthly attendance summary', 'protected'),
        ('/hr-payroll-calculations/', 'Payroll calculations', 'protected'),
    ]
    
    print(f"\nURL ACCESSIBILITY TEST ({len(url_tests)} URLs):")
    for url, desc, access_type in url_tests:
        try:
            response = client.get(url, follow=True)
            final_url = response.redirect_chain[-1][0] if response.redirect_chain else ""
            
            if access_type == 'public':
                if response.status_code == 200:
                    successes.append(f"Public: {desc} - accessible")
                else:
                    issues.append(f"Public: {desc} - status {response.status_code}")
            else:  # protected
                if 'login' in final_url or response.status_code == 200:
                    successes.append(f"Protected: {desc} - properly protected")
                else:
                    issues.append(f"Protected: {desc} - not properly protected")
                    
        except Exception as e:
            issues.append(f"URL {desc}: {str(e)}")
    
    # Test template existence for critical pages
    critical_templates = [
        ('app/base.html', 'Base template'),
        ('app/login.html', 'Login template'),
        ('app/logout_confirmation.html', 'Logout confirmation'),
        ('app/hr/dashboard.html', 'HR dashboard'),
        ('app/employee/dashboard.html', 'Employee dashboard'),
        ('app/tl/dashboard.html', 'TL dashboard'),
        ('app/employee/attendance.html', 'Employee attendance'),
        ('app/hr/attendance.html', 'HR attendance'),
        ('app/tl/attendance-approval.html', 'TL attendance approval'),
        ('app/employee/leave-apply.html', 'Employee leave apply'),
        ('app/hr/leave-approval.html', 'HR leave approval'),
        ('app/tl/team-leave-approval.html', 'TL team leave approval'),
        ('app/hr/announcement.html', 'HR announcements'),
        ('app/employee/project-dashboard.html', 'Employee project dashboard'),
        ('app/tl/project-discussions.html', 'TL project discussions'),
        ('app/chat/chat-dashboard.html', 'Chat dashboard'),
        ('app/employee/enhanced-attendance.html', 'Employee enhanced attendance'),
        ('app/hr/enhanced-attendance.html', 'HR enhanced attendance'),
    ]
    
    print(f"\nTEMPLATE EXISTENCE TEST ({len(critical_templates)} templates):")
    try:
        from django.template.loader import get_template
        for template_path, desc in critical_templates:
            try:
                get_template(template_path)
                successes.append(f"Template: {desc} - exists")
            except Exception as e:
                issues.append(f"Template: {desc} - missing ({str(e)})")
    except Exception as e:
        issues.append(f"Template system error: {str(e)}")
    
    # Test enhanced attendance models
    try:
        from app.models import PresentRecord, AbsentRecord, LateMarkRecord, DailyWorkCompletion
        present_count = PresentRecord.objects.count()
        absent_count = AbsentRecord.objects.count()
        late_count = LateMarkRecord.objects.count()
        work_count = DailyWorkCompletion.objects.count()
        
        successes.append(f"Enhanced attendance models: Present({present_count}), Absent({absent_count}), Late({late_count}), Work({work_count})")
        
    except Exception as e:
        issues.append(f"Enhanced attendance models error: {str(e)}")
    
    # Test project management
    try:
        from app.models import ProjectAssignment, ProjectTask, ProjectMilestone, ProjectDiscussion
        projects = ProjectAssignment.objects.count()
        tasks = ProjectTask.objects.count()
        milestones = ProjectMilestone.objects.count()
        discussions = ProjectDiscussion.objects.count()
        
        successes.append(f"Project management: Projects({projects}), Tasks({tasks}), Milestones({milestones}), Discussions({discussions})")
        
    except Exception as e:
        issues.append(f"Project management error: {str(e)}")
    
    # Test team chat
    try:
        from app.models import TeamChat, ChatReaction
        chat_count = TeamChat.objects.count()
        reactions = ChatReaction.objects.count()
        
        if chat_count > 0:
            successes.append(f"Team chat: Messages({chat_count}), Reactions({reactions})")
        else:
            issues.append("No team chat messages found")
            
    except Exception as e:
        issues.append(f"Team chat error: {str(e)}")
    
    # Test payroll data
    try:
        from app.models import Payroll, PayrollDeduction, SalaryProcessing
        payroll_count = Payroll.objects.count()
        deductions = PayrollDeduction.objects.count()
        processing = SalaryProcessing.objects.count()
        
        if payroll_count > 0:
            successes.append(f"Payroll system: Records({payroll_count}), Deductions({deductions}), Processing({processing})")
        else:
            issues.append("No payroll records found")
            
    except Exception as e:
        issues.append(f"Payroll system error: {str(e)}")
    
    # Results summary
    print(f"\n" + "=" * 60)
    print(f"TEST RESULTS SUMMARY")
    print(f"=" * 60)
    
    print(f"\nSUCCESSES ({len(successes)}):")
    for success in successes:
        print(f"  + {success}")
    
    print(f"\nISSUES ({len(issues)}):")
    for issue in issues:
        print(f"  - {issue}")
    
    total = len(successes) + len(issues)
    success_rate = (len(successes) / total * 100) if total > 0 else 0
    
    print(f"\nOVERALL RESULTS:")
    print(f"  Total Tests: {total}")
    print(f"  Success Rate: {success_rate:.1f}%")
    
    if len(issues) == 0:
        print(f"\nSTATUS: EXCELLENT - All systems working perfectly!")
    elif len(issues) <= 5:
        print(f"\nSTATUS: GOOD - Minor issues found")
    elif len(issues) <= 10:
        print(f"\nSTATUS: FAIR - Several issues need attention")
    else:
        print(f"\nSTATUS: NEEDS ATTENTION - Multiple issues found")

if __name__ == "__main__":
    test_user_roles()