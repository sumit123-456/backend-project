#!/usr/bin/env python3
"""
Simple test to verify template loading without unicode characters
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '.'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.template.loader import get_template

def test_template():
    try:
        template = get_template('app/employee/dashboard.html')
        print("Template loaded successfully!")
        return True
    except Exception as e:
        print(f"Template loading failed: {str(e)}")
        return False

if __name__ == "__main__":
    test_template()