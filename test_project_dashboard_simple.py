#!/usr/bin/env python3
"""
Simple Test for Project Dashboard Enhancement
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append('e:/Backend Project')

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import TestCase, Client
from django.utils import timezone
from datetime import date, timedelta

# Import models
from app.models import Employee, TeamLeader, TeamAssignment, ProjectAssignment, ProjectTask

def test_project_dashboard():
    """Simple test for project dashboard functionality"""
    print("Starting Project Dashboard Test...")
    
    client = Client()
    
    # Create test employee
    employee = Employee.objects.create(
        first_name="Test",
        last_name="Employee",
        email="test@test.com",
        password="test123",
        company_id="TEST001",
        designation="Developer",
        department="IT",
        package=50000.00
    )
    
    # Test login
    response = client.post('/login/', {
        'role': 'employee',
        'email': 'test@test.com',
        'password': 'test123'
    })
    
    if response.status_code == 302:  # Redirect after successful login
        print("✓ Employee login: PASSED")
        
        # Test dashboard access
        dashboard_response = client.get('/employee-project-dashboard/')
        
        if dashboard_response.status_code == 200:
            content = dashboard_response.content.decode('utf-8')
            
            # Check for required elements
            checks = [
                ('Project Dashboard - Test Employee', 'Employee name display'),
                ('Track your assigned projects and communicate with your team', 'Tagline'),
                ('Assigned Projects', 'Statistics section'),
                ('My Projects', 'Projects section'),
                ('My Tasks', 'Tasks section'),
                ('Team Discussions', 'Enhanced button'),
                ('Request Help', 'Help button'),
                ('Refresh', 'Refresh button')
            ]
            
            all_passed = True
            for check_text, description in checks:
                if check_text in content:
                    print(f"✓ {description}: PASSED")
                else:
                    print(f"✗ {description}: FAILED")
                    all_passed = False
            
            if all_passed:
                print("\n=== ALL TESTS PASSED ===")
                print("Enhanced Project Dashboard is working correctly!")
                return True
            else:
                print("\n=== SOME TESTS FAILED ===")
                return False
        else:
            print(f"✗ Dashboard access: FAILED (Status: {dashboard_response.status_code})")
            return False
    else:
        print(f"✗ Employee login: FAILED (Status: {response.status_code})")
        return False

if __name__ == "__main__":
    try:
        success = test_project_dashboard()
        if success:
            print("\nProject Dashboard Enhancement: SUCCESS")
        else:
            print("\nProject Dashboard Enhancement: FAILED")
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"Error during testing: {str(e)}")
        sys.exit(1)