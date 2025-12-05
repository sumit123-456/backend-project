#!/usr/bin/env python3
"""
Test script to verify that the employee dashboard template loads without syntax errors
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.template import engines
from django.template.loader import get_template
from django.test import RequestFactory

def test_template_loading():
    """Test if the template can be loaded and compiled without syntax errors"""
    
    try:
        # Try to load the template
        template = get_template('app/employee/dashboard.html')
        print("✅ Template loaded successfully!")
        
        # Try to create a simple context and render it
        factory = RequestFactory()
        request = factory.get('/employee-dashboard/')
        
        # Minimal context that might be passed to the template
        context = {
            'recent_attendance': [],
            'recent_leave_applications': [],
            'leave_statistics': {},
            'announcements_count': 0,
            'recent_announcements': [],
            'working_days_this_month': 22,
            'present_this_month': 15,
            'attendance_rate': 68.2,
            'pending_leaves': 2,
        }
        
        # Try to render with the context
        rendered = template.render(context, request)
        print("✅ Template rendered successfully!")
        print(f"✅ Rendered content length: {len(rendered)} characters")
        
        return True
        
    except Exception as e:
        print(f"❌ Template loading/rendering failed: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        return False

if __name__ == "__main__":
    print("Testing employee dashboard template...")
    success = test_template_loading()
    
    if success:
        print("\n🎉 All tests passed! The template syntax error has been fixed.")
    else:
        print("\n💥 Template still has issues.")
        sys.exit(1)