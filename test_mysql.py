#!/usr/bin/env python
"""Test MySQL database connection"""
import os
import sys
import django

# Setup Django
sys.path.append('e:/Backend Project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from app.models import Announcement

print("=== TESTING MYSQL CONNECTION ===")
try:
    # Test basic connection
    count = Announcement.objects.count()
    print(f"✅ MySQL Connection: SUCCESS")
    print(f"📊 Total announcements in MySQL: {count}")
    
    # Create test announcement
    print("\n🧪 Creating test announcement...")
    test_ann = Announcement.objects.create(
        title='MySQL Integration Test',
        content='This announcement confirms MySQL integration is working!',
        summary='Test',
        category='general',
        priority='medium',
        status='published',
        target_audience='all',
        target_departments=[],
        target_locations=[],
        target_roles=[],
        created_by='MySQL Test',
        author_designation='System',
        author_department='Testing',
        tags=[],
        comments=''
    )
    
    print(f"✅ Created announcement with ID: {test_ann.id}")
    print(f"📊 New total count: {Announcement.objects.count()}")
    
    # Show recent announcements
    recent = Announcement.objects.all().order_by('-id')[:3]
    print("\n📝 Recent announcements:")
    for ann in recent:
        print(f"  - ID {ann.id}: {ann.title} (Created: {ann.created_at})")
    
    # Clean up test
    test_ann.delete()
    print(f"\n🧹 Cleanup: Removed test announcement")
    print(f"📊 Final count: {Announcement.objects.count()}")
    
    print("\n🎉 MySQL INTEGRATION: WORKING PERFECTLY!")
    
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()