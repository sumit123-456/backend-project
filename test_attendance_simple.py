#!/usr/bin/env python3
"""
Simple test to verify attendance table public access functionality
"""
import os
import sys
import django

# Setup Django environment
sys.path.append('e:/Backend Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.test import Client
from django.urls import reverse

def test_attendance_table_access():
    """Test that attendance table can be accessed without login"""
    print("Testing Attendance Table Public Access...")
    
    # Create a test client
    client = Client()
    
    # Test access without login
    print("Testing page access without login...")
    try:
        response = client.get(reverse('attendance-table'))
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("SUCCESS: Page accessible without login")
            
            # Check content
            content = response.content.decode('utf-8')
            
            if 'Authentication Required' in content:
                print("SUCCESS: Authentication message displayed")
            else:
                print("WARNING: Authentication message not found")
                
            if 'Login' in content:
                print("SUCCESS: Login link found")
            else:
                print("WARNING: Login link not found")
                
        else:
            print(f"FAILED: Page returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"ERROR: {str(e)}")
        return False
    
    print("Test completed successfully!")
    return True

if __name__ == "__main__":
    test_attendance_table_access()