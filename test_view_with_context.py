#!/usr/bin/env python3
"""
Test the actual view function with proper context
"""

import os
import sys
import django
from datetime import date, datetime

# Add the current directory to Python path
sys.path.append('.')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.sessions.backends.db import SessionStore
from app.views import hr_enhanced_attendance_view
from app.models import HRProfile, PresentRecord, AbsentRecord, LateMarkRecord, DailyWorkCompletion

def test_view_with_context():
    """Test the view with proper context and session"""
    
    print("Testing HR Enhanced Attendance View with proper context...")
    
    try:
        # Get HR profile
        hr = HRProfile.objects.first()
        if not hr:
            print("No HR profile found")
            return False
            
        print(f"Found HR: {hr.full_name}")
        
        # Create a session
        session = SessionStore()
        session['hr_id'] = hr.id
        session['role'] = 'hr'
        session['hr_name'] = hr.full_name
        session.save()
        
        # Create a proper request
        factory = RequestFactory()
        request = factory.get('/hr-enhanced-attendance/')
        
        # Attach the session to the request
        request.session = session
        
        # Test the view function directly
        print("Calling hr_enhanced_attendance_view...")
        response = hr_enhanced_attendance_view(request)
        
        print(f"Response status: {response.status_code}")
        print(f"Response type: {type(response)}")
        
        if response.status_code == 200:
            print("View executed successfully!")
            # Check if response has content
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                print(f"Content length: {len(content)} characters")
                if len(content) < 100:
                    print("Content seems too short:")
                    print(content[:200])
                else:
                    print("Content looks good!")
            return True
        else:
            print(f"View returned error status: {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                print(f"Error content: {content[:500]}")
            return False
            
    except Exception as e:
        print(f"Error calling view: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

def check_models():
    """Check if the models exist and have data"""
    
    print("\nChecking model data...")
    
    try:
        # Check basic models
        employees = Employee.objects.count()
        present_records = PresentRecord.objects.count()
        absent_records = AbsentRecord.objects.count()
        late_mark_records = LateMarkRecord.objects.count()
        work_completions = DailyWorkCompletion.objects.count()
        
        print(f"Employees: {employees}")
        print(f"Present records: {present_records}")
        print(f"Absent records: {absent_records}")
        print(f"Late mark records: {late_mark_records}")
        print(f"Work completions: {work_completions}")
        
        return True
        
    except Exception as e:
        print(f"Error checking models: {str(e)}")
        return False

if __name__ == "__main__":
    # Import Employee here to avoid circular imports
    from app.models import Employee
    
    success1 = check_models()
    success2 = test_view_with_context()
    
    if success1 and success2:
        print("\nAll tests passed!")
    else:
        print("\nSome tests failed!")