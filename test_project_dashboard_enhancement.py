#!/usr/bin/env python3
"""
Test Project Dashboard Enhancement
Verifies that the enhanced project dashboard features are working correctly
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
from django.contrib import messages
from django.contrib.sessions.middleware import SessionMiddleware
from django.contrib.auth.middleware import AuthenticationMiddleware
from django.contrib.messages.middleware import MessageMiddleware
from django.contrib.messages.storage.fallback import FallbackStorage
from django.utils import timezone
from datetime import date, timedelta
import json

# Import models
from app.models import Employee, TeamLeader, TeamAssignment, ProjectAssignment, ProjectTask

class ProjectDashboardTestCase(TestCase):
    """Test the enhanced project dashboard functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test employee
        self.employee = Employee.objects.create(
            first_name="John",
            last_name="Doe",
            email="john.doe@test.com",
            password="test123",
            company_id="EMP001",
            designation="Software Developer",
            department="IT",
            package=50000.00
        )
        
        # Create test team leader
        self.tl_employee = Employee.objects.create(
            first_name="Jane",
            last_name="Smith",
            email="jane.smith@test.com",
            password="test123",
            company_id="TL001",
            designation="Team Leader",
            department="IT",
            package=70000.00
        )
        
        self.team_leader = TeamLeader.objects.create(
            employee=self.tl_employee,
            experience_years=5,
            team_size="5-10",
            responsibilities="Project management and team coordination"
        )
        
        # Create team assignment
        TeamAssignment.objects.create(
            team_leader=self.team_leader,
            employee=self.employee,
            role="Developer",
            assignment_date=date.today()
        )
        
        # Create test project
        self.project = ProjectAssignment.objects.create(
            project_name="Test Project",
            project_code="TEST001",
            team_leader=self.team_leader,
            priority="high",
            start_date=date.today(),
            end_date=date.today() + timedelta(days=30),
            description="A test project for dashboard testing"
        )
        
        # Add employee to project team
        self.project.team_members.add(self.employee)
        
        # Create test tasks
        ProjectTask.objects.create(
            project=self.project,
            assigned_to=self.employee,
            assigned_by=self.team_leader,
            title="Test Task 1",
            description="Complete test task 1",
            task_status="in_progress",
            priority="high",
            start_date=timezone.now(),
            due_date=timezone.now() + timedelta(days=7),
            estimated_hours=8.0,
            progress_percentage=50
        )
        
        ProjectTask.objects.create(
            project=self.project,
            assigned_to=self.employee,
            assigned_by=self.team_leader,
            title="Test Task 2",
            description="Complete test task 2",
            task_status="completed",
            priority="medium",
            start_date=timezone.now() - timedelta(days=5),
            due_date=timezone.now() - timedelta(days=1),
            estimated_hours=4.0,
            progress_percentage=100,
            completed_at=timezone.now() - timedelta(days=1)
        )
    
    def test_employee_login_and_session(self):
        """Test employee login and session creation"""
        # Simulate login
        response = self.client.post('/login/', {
            'role': 'employee',
            'email': 'john.doe@test.com',
            'password': 'test123'
        }, follow=True)
        
        # Check if session was created
        self.assertEqual(self.client.session['employee_id'], self.employee.id)
        self.assertEqual(self.client.session['employee_name'], 'John Doe')
        self.assertEqual(self.client.session['role'], 'employee')
        
        print("✅ Employee login and session creation: PASSED")
    
    def test_project_dashboard_access(self):
        """Test accessing the project dashboard"""
        # Login first
        self.client.post('/login/', {
            'role': 'employee',
            'email': 'john.doe@test.com',
            'password': 'test123'
        })
        
        # Access project dashboard
        response = self.client.get('/employee-project-dashboard/')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Project Dashboard - John Doe')
        self.assertContains(response, 'Track your assigned projects and communicate with your team')
        self.assertContains(response, 'Assigned Projects')
        self.assertContains(response, 'Active Projects')
        self.assertContains(response, 'Completed Tasks')
        self.assertContains(response, 'Pending Tasks')
        
        print("✅ Project dashboard access and content: PASSED")
    
    def test_project_data_display(self):
        """Test that project data is displayed correctly"""
        # Login first
        self.client.post('/login/', {
            'role': 'employee',
            'email': 'john.doe@test.com',
            'password': 'test123'
        })
        
        # Access project dashboard
        response = self.client.get('/employee-project-dashboard/')
        
        # Check that project information is displayed
        self.assertContains(response, 'Test Project')
        self.assertContains(response, 'TEST001')
        self.assertContains(response, 'High')
        self.assertContains(response, 'Active')
        
        # Check for enhanced features
        self.assertContains(response, 'Team Discussions')
        self.assertContains(response, 'Request Help')
        self.assertContains(response, 'Refresh')
        
        print("✅ Project data display and enhanced features: PASSED")
    
    def test_task_data_display(self):
        """Test that task data is displayed correctly"""
        # Login first
        self.client.post('/login/', {
            'role': 'employee',
            'email': 'john.doe@test.com',
            'password': 'test123'
        })
        
        # Access project dashboard
        response = self.client.get('/employee-project-dashboard/')
        
        # Check that tasks are displayed
        self.assertContains(response, 'My Tasks')
        self.assertContains(response, 'Test Task 1')
        self.assertContains(response, 'Test Task 2')
        self.assertContains(response, 'In Progress')
        self.assertContains(response, 'Completed')
        
        print("✅ Task data display: PASSED")
    
    def test_date_format_display(self):
        """Test that the current date is displayed correctly"""
        # Login first
        self.client.post('/login/', {
            'role': 'employee',
            'email': 'john.doe@test.com',
            'password': 'test123'
        })
        
        # Access project dashboard
        response = self.client.get('/employee-project-dashboard/')
        
        # Check date format
        today = timezone.now()
        expected_date_format = today.strftime('%B %d, %Y')
        self.assertContains(response, expected_date_format)
        
        print(f"✅ Date format display ({expected_date_format}): PASSED")
    
    def test_session_employee_name_fallback(self):
        """Test the employee name fallback in session"""
        # Test with empty session
        self.client.session.flush()
        
        # Access dashboard without login
        response = self.client.get('/employee-project-dashboard/')
        
        # Should redirect to login due to authentication check
        self.assertEqual(response.status_code, 302)
        
        # Login and test default name
        self.client.post('/login/', {
            'role': 'employee',
            'email': 'john.doe@test.com',
            'password': 'test123'
        })
        
        # Clear employee name from session to test fallback
        self.client.session['employee_name'] = None
        
        # Access dashboard
        response = self.client.get('/employee-project-dashboard/')
        
        # Check that it falls back to "Employee"
        self.assertContains(response, 'Project Dashboard - Employee')
        
        print("✅ Session employee name fallback: PASSED")

def run_tests():
    """Run all project dashboard tests"""
    print("🚀 Starting Project Dashboard Enhancement Tests...")
    print("=" * 60)
    
    # Run the tests
    test_case = ProjectDashboardTestCase()
    test_case.setUp()
    
    try:
        test_case.test_employee_login_and_session()
        test_case.test_project_dashboard_access()
        test_case.test_project_data_display()
        test_case.test_task_data_display()
        test_case.test_date_format_display()
        test_case.test_session_employee_name_fallback()
        
        print("=" * 60)
        print("🎉 All Project Dashboard Enhancement Tests: PASSED")
        print("\n📋 Summary:")
        print("   • Employee session management")
        print("   • Project dashboard access")
        print("   • Project data display")
        print("   • Task data display")
        print("   • Date formatting")
        print("   • Session fallback handling")
        print("\n✅ Enhanced Project Dashboard is working correctly!")
        
    except Exception as e:
        print("=" * 60)
        print(f"❌ Test Failed: {str(e)}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)