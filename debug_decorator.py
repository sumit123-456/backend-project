#!/usr/bin/env python3
"""
Direct test of the view without session
"""

import os
import sys
import django

# Add the current directory to Python path
sys.path.append('.')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from app.views import hr_enhanced_attendance_view
from app.models import HRProfile, Employee
from django.contrib.sessions.backends.db import SessionStore

def test_decorator():
    """Test the login decorator directly"""
    
    print("Testing login decorator...")
    
    try:
        # Check if we have an HR profile
        hr = HRProfile.objects.first()
        if not hr:
            print("No HR profile found")
            return False
            
        print(f"Found HR: {hr.full_name}")
        
        # Create a session and set HR ID
        session = SessionStore()
        session['hr_id'] = hr.id
        session['role'] = 'hr'
        session['hr_name'] = hr.full_name
        session.save()
        
        print(f"Session created with key: {session.session_key}")
        
        # Try to access session data manually
        print(f"Session data: {dict(session)}")
        
        # Create a simple mock request
        class MockRequest:
            def __init__(self):
                self.session = session
                self.META = {}
                self.method = 'GET'
                self.GET = {}
                self.POST = {}
                
        mock_request = MockRequest()
        
        # Test session access
        print(f"HR ID from session: {mock_request.session.get('hr_id')}")
        print(f"Role from session: {mock_request.session.get('role')}")
        
        return True
        
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_decorator()