#!/usr/bin/env python
import os
import sys
import django

# Setup Django
sys.path.append('e:/Backend Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from app.models import HRProfile, Employee, PresentRecord, AbsentRecord, LateMarkRecord, DailyWorkCompletion
from app.views import hr_enhanced_attendance_view
from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware

def test_hr_attendance_view():
    print("=== Testing HR Enhanced Attendance View ===")
    
    # Check database status
    print("\n--- Database Status ---")
    print(f"HR Profiles: {HRProfile.objects.count()}")
    print(f"Employees: {Employee.objects.count()}")
    print(f"Present Records: {PresentRecord.objects.count()}")
    print(f"Absent Records: {AbsentRecord.objects.count()}")
    print(f"Late Mark Records: {LateMarkRecord.objects.count()}")
    print(f"Work Completions: {DailyWorkCompletion.objects.count()}")
    
    # Check if we have an HR profile
    hr = HRProfile.objects.first()
    if not hr:
        print("\n❌ No HR profiles found in database!")
        return False
    
    print(f"\n--- Using HR Profile ---")
    print(f"HR: {hr.full_name} (ID: {hr.id})")
    
    # Create a mock request
    factory = RequestFactory()
    request = factory.get('/hr-enhanced-attendance/')
    
    # Add session middleware manually
    middleware = SessionMiddleware(lambda x: x)
    middleware.process_request(request)
    request.session.save()
    
    # Set HR ID in session
    request.session['hr_id'] = hr.id
    request.session['role'] = 'hr'
    request.session['hr_name'] = hr.full_name
    
    print(f"\n--- Session Data ---")
    print(f"HR ID: {request.session.get('hr_id')}")
    print(f"Role: {request.session.get('role')}")
    
    try:
        print(f"\n--- Calling View Function ---")
        response = hr_enhanced_attendance_view(request)
        
        print(f"Response type: {type(response)}")
        print(f"Response status code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ View executed successfully!")
            
            # Check if response has content
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                print(f"Content length: {len(content)} characters")
                
                # Check for key template elements
                key_elements = [
                    'Enhanced Attendance Management',
                    'total_employees',
                    'present_records',
                    'absent_records',
                    'late_mark_records',
                    'work_completions'
                ]
                
                for element in key_elements:
                    if element in content:
                        print(f"✅ Found '{element}' in template")
                    else:
                        print(f"❌ Missing '{element}' in template")
                
            return True
        else:
            print(f"❌ View returned status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error calling view: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_hr_attendance_view()