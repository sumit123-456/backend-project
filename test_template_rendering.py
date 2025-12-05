#!/usr/bin/env python3
"""
Test template rendering
"""

import os
import sys
import django

# Add the current directory to Python path
sys.path.append('.')

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.template.loader import get_template
from django.test import RequestFactory
from app.models import HRProfile

def test_template_rendering():
    """Test if template renders properly"""
    
    print("Testing template rendering...")
    
    try:
        # Get HR profile
        hr = HRProfile.objects.first()
        if not hr:
            print("No HR profile found")
            return False
            
        print(f"Found HR: {hr.full_name}")
        
        # Create test context
        context = {
            'hr': hr,
            'employees': [],
            'present_records': [],
            'absent_records': [],
            'late_mark_records': [],
            'work_completions': [],
            'from_date': None,
            'to_date': None,
            'total_employees': 0,
            'total_present': 0,
            'total_absent': 0,
            'total_late_mark': 0,
        }
        
        # Try to render the template
        print("Loading template...")
        template = get_template('app/hr/enhanced-attendance.html')
        
        print("Rendering template...")
        rendered = template.render(context)
        
        print(f"Template rendered successfully!")
        print(f"Content length: {len(rendered)} characters")
        
        if len(rendered) > 100:
            print("Template appears to have content")
            # Print first 500 chars
            print("First 500 characters:")
            print(rendered[:500])
            return True
        else:
            print("Template seems to be too short")
            print(f"Content: {rendered}")
            return False
            
    except Exception as e:
        print(f"Error rendering template: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_template_rendering()
    if success:
        print("\nTemplate rendering test passed!")
    else:
        print("\nTemplate rendering test failed!")