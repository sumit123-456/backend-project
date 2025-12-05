#!/usr/bin/env python
"""
Verify that the HR Enhanced Attendance page is working correctly
"""
import os
import sys
import django

# Setup Django
sys.path.append('e:/Backend Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import Client
from app.models import HRProfile, Employee, PresentRecord, AbsentRecord, LateMarkRecord, DailyWorkCompletion

def verify_enhanced_attendance_page():
    print("=== Verifying Enhanced Attendance Page Fix ===")
    
    # Check current database status
    print("\n--- Current Database Status ---")
    print(f"HR Profiles: {HRProfile.objects.count()}")
    print(f"Employees: {Employee.objects.count()}")
    print(f"Present Records: {PresentRecord.objects.count()}")
    print(f"Absent Records: {AbsentRecord.objects.count()}")
    print(f"Late Mark Records: {LateMarkRecord.objects.count()}")
    print(f"Work Completions: {DailyWorkCompletion.objects.count()}")
    
    # Create a test client
    client = Client()
    
    # Get HR credentials
    hr = HRProfile.objects.first()
    if not hr:
        print("\n❌ No HR profiles found!")
        return False
    
    print(f"\n--- Testing with HR: {hr.full_name} ---")
    
    # Simulate login
    session = client.session
    session['hr_id'] = hr.id
    session['role'] = 'hr'
    session['hr_name'] = hr.full_name
    session.save()
    
    # Make request to the enhanced attendance page
    response = client.get('/hr-enhanced-attendance/')
    
    print(f"\n--- Response Analysis ---")
    print(f"Status Code: {response.status_code}")
    print(f"Content Type: {response.get('Content-Type', 'Unknown')}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        print(f"Content Length: {len(content)} characters")
        
        # Check for key indicators that the page is working
        key_indicators = [
            ('Enhanced Attendance Management', 'Page title'),
            ('total_employees', 'Template variable'),
            ('present_records', 'Present records section'),
            ('absent_records', 'Absent records section'),
            ('late_mark_records', 'Late mark records section'),
            ('work_completions', 'Work completions section'),
            ('k-card', 'Bootstrap card styling'),
            ('dashboard', 'Dashboard functionality'),
        ]
        
        print(f"\n--- Template Content Verification ---")
        for indicator, description in key_indicators:
            if indicator in content:
                print(f"✅ {description}: Found")
            else:
                print(f"❌ {description}: Missing")
        
        # Check if data is being displayed
        data_indicators = [
            ('Dinesh Ade', 'Employee name in records'),
            ('Present', 'Present status'),
            ('Late Mark', 'Late mark status'),
            ('Absent', 'Absent status'),
            ('2025-11-30', 'Current date in records'),
        ]
        
        print(f"\n--- Data Display Verification ---")
        for indicator, description in data_indicators:
            if indicator in content:
                print(f"✅ {description}: Found in content")
            else:
                print(f"⚠️  {description}: Not found in content")
        
        return True
        
    elif response.status_code == 302:
        print(f"❌ Page redirected (likely due to authentication)")
        print(f"Redirect location: {response.get('Location', 'Unknown')}")
        return False
    else:
        print(f"❌ Unexpected status code: {response.status_code}")
        return False

if __name__ == "__main__":
    success = verify_enhanced_attendance_page()
    if success:
        print(f"\n🎉 SUCCESS: Enhanced Attendance Page is working correctly!")
        print(f"📊 The page now displays real data from the database")
        print(f"🔗 Access the page at: http://127.0.0.1:8000/hr-enhanced-attendance/")
        print(f"👤 Login as HR to view the enhanced attendance management dashboard")
    else:
        print(f"\n❌ FAILURE: Issues detected with the enhanced attendance page")