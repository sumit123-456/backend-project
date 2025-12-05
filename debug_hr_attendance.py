#!/usr/bin/env python3
"""
Debug script to test HR Enhanced Attendance view
"""

import os
import sys
import django

# Add the current directory to Python path
sys.path.append('.')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from app.views import hr_enhanced_attendance_view
from app.models import HRProfile

def test_hr_attendance_view():
    """Test the HR enhanced attendance view"""
    
    print("Testing HR Enhanced Attendance View...")
    
    # Create a request factory
    factory = RequestFactory()
    
    # Create a request
    request = factory.get('/hr-enhanced-attendance/')
    
    # Add session middleware
    middleware = SessionMiddleware(lambda x: x)
    request = middleware.process_request(request)
    
    # Set session data
    request.session['hr_id'] = 1
    request.session['role'] = 'hr'
    
    try:
        # Test if HR exists
        hr = HRProfile.objects.first()
        if not hr:
            print("No HR profile found in database")
            return False
            
        print(f"Found HR profile: {hr.full_name}")
        
        # Update session with actual HR ID
        request.session['hr_id'] = hr.id
        
        # Call the view
        print("Calling hr_enhanced_attendance_view...")
        response = hr_enhanced_attendance_view(request)
        
        # Check response
        print(f"Response status: {response.status_code}")
        print(f"Response type: {type(response)}")
        
        if response.status_code == 200:
            print("View executed successfully!")
            # Get the rendered content
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                print(f"Content length: {len(content)} characters")
                if len(content) < 100:
                    print("Content seems too short:")
                    print(content)
                else:
                    print("Content looks good!")
            return True
        else:
            print(f"View returned error status: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"Error calling view: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_hr_attendance_view()
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")