#!/usr/bin/env python
"""
Simple System Health Check
"""
import os
import sys
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()
from django.test import Client
from app.models import Employee, HRProfile, TeamLeader, TeamAssignment, PresentRecord, AbsentRecord, LateMarkRecord, LeaveApply, Payroll, Announcement, ProjectAssignment

def test():
    print("HR SYSTEM TEST")
    print("="*50)
    issues = []
    ok = []
    
    # Database test
    try:
        emp_count = Employee.objects.count()
        hr_count = HRProfile.objects.count() 
        tl_count = TeamLeader.objects.count()
        ok.append(f"Database OK - {emp_count} employees, {hr_count} HR, {tl_count} TL")
    except Exception as e:
        issues.append(f"Database Error: {e}")
    
    # URLs test
    client = Client()
    urls = [('/', 'Login'), ('/create-hr/', 'Create HR'), ('/hr-list/', 'HR List')]
    for url, desc in urls:
        try:
            resp = client.get(url)
            if resp.status_code == 200:
                ok.append(f"{desc} page accessible")
            else:
                issues.append(f"{desc} page returned {resp.status_code}")
        except Exception as e:
            issues.append(f"{desc} error: {e}")
    
    # Attendance test
    try:
        present = PresentRecord.objects.count()
        absent = AbsentRecord.objects.count()
        late = LateMarkRecord.objects.count()
        if present > 0 or absent > 0 or late > 0:
            ok.append(f"Attendance working ({present}P, {absent}A, {late}L)")
        else:
            issues.append("No attendance records")
    except Exception as e:
        issues.append(f"Attendance error: {e}")
        
    # Leave test
    try:
        leaves = LeaveApply.objects.count()
        pending = LeaveApply.objects.filter(status='pending').count()
        ok.append(f"Leave system OK - {leaves} apps ({pending} pending)")
    except Exception as e:
        issues.append(f"Leave error: {e}")
        
    # Payroll test
    try:
        payroll = Payroll.objects.count()
        if payroll > 0:
            ok.append(f"Payroll OK - {payroll} records")
        else:
            issues.append("No payroll records")
    except Exception as e:
        issues.append(f"Payroll error: {e}")
        
    # Templates test
    try:
        from django.template.loader import get_template
        templates = ['app/base.html', 'app/login.html', 'app/hr/dashboard.html']
        for t in templates:
            get_template(t)
            ok.append(f"Template {t} exists")
    except Exception as e:
        issues.append(f"Template error: {e}")
        
    # Results
    print(f"\nOK ({len(ok)}):")
    for item in ok:
        print(f"  + {item}")
        
    print(f"\nISSUES ({len(issues)}):")
    for item in issues:
        print(f"  - {item}")
        
    total = len(ok) + len(issues)
    rate = len(ok) / total * 100 if total > 0 else 0
    print(f"\nSUMMARY: {rate:.1f}% success rate")
    
    if len(issues) == 0:
        print("SYSTEM HEALTH: EXCELLENT")
    elif len(issues) <= 3:
        print("SYSTEM HEALTH: GOOD") 
    else:
        print("SYSTEM HEALTH: NEEDS ATTENTION")

if __name__ == "__main__":
    test()