#!/usr/bin/env python
"""
Test script to verify that the enhanced attendance template renders without syntax errors.
"""
import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, 'e:/Backend Project')

# Set up Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.template.loader import get_template
from django.template import Context

def test_enhanced_attendance_template():
    """Test that the enhanced attendance content template renders without errors."""
    try:
        # Load the template
        template = get_template('app/enhanced_attendance_content.html')
        
        # Create a sample context (mimicking what would be passed to the template)
        context_data = {
            'user_role': 'Employee',
            'present_today': None,
            'absent_today': None,
            'late_mark_today': None,
            'has_marked_attendance': False,
            'current_time': None,
            'is_office_closing_time': False,
            'work_completion_today': None,
            'total_employees': 0,
            'total_present': 0,
            'total_absent': 0,
            'total_late_mark': 0,
            'present_records': [],
            'absent_records': [],
            'late_mark_records': [],
        }
        
        # Try to render the template
        rendered_content = template.render(context_data)
        
        print("SUCCESS: Template rendered successfully!")
        print(f"Rendered content length: {len(rendered_content)} characters")
        print("No template syntax errors detected")
        return True
        
    except Exception as e:
        print(f"ERROR: Template rendering failed: {str(e)}")
        return False

if __name__ == "__main__":
    print("Testing enhanced_attendance_content.html template...")
    success = test_enhanced_attendance_template()
    
    if success:
        print("\nSUCCESS: Template fix verification completed successfully!")
    else:
        print("\nFAILURE: Template still has issues")
        sys.exit(1)