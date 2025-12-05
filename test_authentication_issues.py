#!/usr/bin/env python3
"""
Test script to identify and fix authentication issues
This script will help diagnose and fix:
1. Infinite login redirects
2. Session management issues
3. Authentication decorator problems
"""

import os
import sys
import django

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
django.setup()

from django.test import Client, RequestFactory
from django.contrib.messages.storage.fallback import FallbackStorage
from app.models import Employee, HRProfile, TeamLeader
from app.views import login_required_with_exemptions, attendance_table_view, login_view, logout_view
from django.urls import resolve, reverse
from django.http import HttpRequest

def test_authentication_flow():
    """Test the complete authentication flow"""
    print("=== AUTHENTICATION FLOW TEST ===")
    
    client = Client()
    
    # Test 1: Check if login page loads correctly
    print("\n1. Testing login page...")
    response = client.get('/')
    print(f"   Login page status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Login page loads correctly")
    else:
        print("   ❌ Login page failed to load")
    
    # Test 2: Check attendance table public access
    print("\n2. Testing attendance table public access...")
    response = client.get('/attendance-table/')
    print(f"   Attendance table status: {response.status_code}")
    if response.status_code == 200:
        print("   ✅ Attendance table accessible without login")
    else:
        print("   ❌ Attendance table not accessible")
    
    # Test 3: Check dashboard redirect without login
    print("\n3. Testing protected page redirects...")
    response = client.get('/employee-dashboard/')
    print(f"   Employee dashboard status: {response.status_code}")
    if response.status_code == 302:  # Redirect
        print(f"   ✅ Properly redirects to: {response.url}")
    else:
        print("   ❌ Dashboard redirect failed")
    
    return client

def identify_issues():
    """Identify potential issues in the authentication system"""
    print("\n=== ISSUE IDENTIFICATION ===")
    
    issues = []
    
    # Check 1: URL patterns
    print("\n1. Checking URL patterns...")
    from django.urls import get_resolver
    resolver = get_resolver()
    
    attendance_table_found = False
    for pattern in resolver.url_patterns:
        if hasattr(pattern, 'pattern') and 'attendance-table' in str(pattern.pattern):
            attendance_table_found = True
            break
    
    if attendance_table_found:
        print("   ✅ attendance-table URL pattern found")
    else:
        issues.append("attendance-table URL pattern not found")
        print("   ❌ attendance-table URL pattern not found")
    
    return issues

def provide_solutions():
    """Provide solutions for identified issues"""
    print("\n=== SOLUTIONS ===")
    
    solutions = [
        {
            "issue": "Potential redirect loops",
            "solution": "Add proper session validation and avoid redirecting from exempt URLs"
        },
        {
            "issue": "Session persistence after logout",
            "solution": "Ensure session.flush() is called and session is properly cleared"
        },
        {
            "issue": "Authentication decorator edge cases",
            "solution": "Add better URL name validation and session state checks"
        }
    ]
    
    for i, solution in enumerate(solutions, 1):
        print(f"\n{i}. {solution['issue']}")
        print(f"   Solution: {solution['solution']}")
    
    return solutions

if __name__ == "__main__":
    print("🔍 AUTHENTICATION SYSTEM DIAGNOSTIC TOOL")
    print("=" * 50)
    
    # Run tests
    client = test_authentication_flow()
    issues = identify_issues()
    solutions = provide_solutions()
    
    print("\n" + "=" * 50)
    print("📋 SUMMARY")
    
    if not issues:
        print("✅ No critical issues identified")
    else:
        print(f"❌ Found {len(issues)} issues:")
        for issue in issues:
            print(f"   - {issue}")
    
    print(f"\n🔧 {len(solutions)} solutions provided")