#!/usr/bin/env python3
"""
Simple debug script to test HR Enhanced Attendance view
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
from app.views import hr_enhanced_attendance_view
from app.models import HRProfile

def test_hr_attendance_simple():
    """Test the HR enhanced attendance view - simple version"""
    
    print("Testing HR Enhanced Attendance View - Simple...")
    
    # Create a request factory
    factory = RequestFactory()
    
    # Create a request with GET parameters
    request = factory.get('/hr-enhanced-attendance/?from_date=2025-11-01&to_date=2025-11-30')
    
    try:
        # Test if HR exists
        hr = HRProfile.objects.first()
        if not hr:
            print("No HR profile found in database")
            return False
            
        print(f"Found HR profile: {hr.full_name}")
        
        # Test basic view functionality
        print("Testing view function directly...")
        
        # Manually call the function with proper setup
        from django.contrib.sessions.middleware import SessionMiddleware
        
        # Create middleware and process request
        middleware = SessionMiddleware(lambda x: x)
        request = middleware.process_request(request)
        
        # Set session data
        request.session['hr_id'] = hr.id
        request.session['role'] = 'hr'
        
        print("Calling hr_enhanced_attendance_view...")
        response = hr_enhanced_attendance_view(request)
        
        print(f"Response status: {response.status_code}")
        print(f"Response type: {type(response)}")
        
        if response.status_code == 200:
            print("View executed successfully!")
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

if __name__ == "__main__":
    success = test_hr_attendance_simple()
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nTest failed!")