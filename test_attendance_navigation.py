#!/usr/bin/env python3
"""
Test script for Day-wise Attendance Table Previous Page Navigation
Tests enhanced navigation functionality, referrer tracking, and data preservation.
"""

import os
import sys
import django
import requests
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from app.models import Employee

class AttendanceNavigationTest(TestCase):
    """Test attendance table navigation functionality"""
    
    def setUp(self):
        """Set up test data"""
        self.client = Client()
        
        # Create test employee
        self.employee = Employee.objects.create(
            first_name="Test",
            last_name="Employee",
            company_id="TEST001",
            email="test@example.com",
            password="testpass",
            designation="Developer",
            department="IT"
        )
        
        # Create session for employee
        session = self.client.session
        session['employee_id'] = self.employee.id
        session['role'] = 'Employee'
        session.save()
    
    def test_attendance_table_access(self):
        """Test basic attendance table access"""
        response = self.client.get(reverse('attendance-table'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Day-wise Attendance Table')
    
    def test_referrer_tracking(self):
        """Test referrer tracking in session"""
        # Simulate navigation from enhanced attendance
        referrer_url = "http://testserver/enhanced-attendance/"
        
        # First visit enhanced attendance page
        self.client.get(reverse('enhanced-attendance'))
        
        # Then visit attendance table
        response = self.client.get(
            reverse('attendance-table'),
            HTTP_REFERER=referrer_url
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Previous Page')
        self.assertContains(response, 'Day-wise Attendance Table')
    
    def test_pagination_functionality(self):
        """Test pagination with different page sizes"""
        # Test default page size
        response = self.client.get(reverse('attendance-table'))
        self.assertEqual(response.status_code, 200)
        
        # Test custom page size
        response = self.client.get(
            reverse('attendance-table') + '?page=50&page_num=1'
        )
        self.assertEqual(response.status_code, 200)
    
    def test_filter_preservation(self):
        """Test filter form preservation"""
        from_date = '2024-01-01'
        to_date = '2024-01-31'
        
        response = self.client.get(
            reverse('attendance-table'),
            {
                'from_date': from_date,
                'to_date': to_date,
                'page': 20
            }
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, from_date)
        self.assertContains(response, to_date)
    
    def test_enhanced_attendance_navigation(self):
        """Test navigation between enhanced attendance and table"""
        # Visit enhanced attendance
        response1 = self.client.get(reverse('enhanced-attendance'))
        self.assertEqual(response1.status_code, 200)
        
        # Visit attendance table with referrer
        response2 = self.client.get(
            reverse('attendance-table'),
            HTTP_REFERER='http://testserver/enhanced-attendance/'
        )
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, 'Previous Page')
    
    def test_breadcrumb_navigation(self):
        """Test breadcrumb navigation display"""
        response = self.client.get(
            reverse('attendance-table'),
            HTTP_REFERER='http://testserver/enhanced-attendance/'
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'breadcrumb')
        self.assertContains(response, 'Previous Page')

def run_navigation_tests():
    """Run all navigation tests"""
    print("🧪 Running Attendance Navigation Tests...")
    print("=" * 50)
    
    # Create test suite
    from django.test.utils import get_runner
    from django.conf import settings
    
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=False, keepdb=False)
    
    # Run tests
    failures = test_runner.run_tests(["test_attendance_navigation"])
    
    if failures:
        print(f"\n❌ {failures} test(s) failed")
        return False
    else:
        print(f"\n✅ All navigation tests passed!")
        return True

if __name__ == "__main__":
    try:
        success = run_navigation_tests()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)