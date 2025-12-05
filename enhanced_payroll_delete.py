#!/usr/bin/env python
"""
Enhanced Payroll Deletion System
Provides robust payroll deletion with comprehensive error handling
"""
import os
import sys
import django
import json
import logging
import re
from datetime import datetime

# Add the project directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from django.db import transaction
from django.db.models import Q
from app.models import Payroll, Employee, PayrollDeduction, SalaryProcessing, MonthlyAttendanceSummary
from django.core.management.base import BaseCommand
from django.contrib import messages

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('payroll_deletion.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedPayrollDeletion:
    """
    Enhanced Payroll Deletion Class
    Provides comprehensive payroll deletion with error handling
    """
    
    def __init__(self):
        self.deletion_stats = {
            'total_processed': 0,
            'successful_deletions': 0,
            'failed_deletions': 0,
            'json_records_found': 0,
            'related_records_cleaned': 0
        }
    
    def validate_payroll_deletion(self, payroll_id):
        """
        Validate that a payroll record can be safely deleted
        """
        try:
            payroll = Payroll.objects.get(id=payroll_id)
            
            # Check if payroll exists
            if not payroll:
                return False, "Payroll record not found"
            
            # Check if payroll is processed (optional: you might want to prevent deletion of processed payrolls)
            if payroll.is_processed:
                logger.warning(f"Attempting to delete processed payroll ID: {payroll_id}")
            
            # Check for related records
            related_deductions = PayrollDeduction.objects.filter(payroll=payroll).count()
            related_processing = SalaryProcessing.objects.filter(payroll_record=payroll).count()
            related_summaries = MonthlyAttendanceSummary.objects.filter(
                employee=payroll.employee,
                month=payroll.month,
                year=payroll.year
            ).count()
            
            validation_result = {
                'payroll_exists': True,
                'employee': f"{payroll.employee.first_name} {payroll.employee.last_name}",
                'period': f"{payroll.month} {payroll.year}",
                'is_processed': payroll.is_processed,
                'related_deductions': related_deductions,
                'related_processing': related_processing,
                'related_summaries': related_summaries,
                'can_delete': True
            }
            
            return True, validation_result
            
        except Payroll.DoesNotExist:
            return False, "Payroll record not found"
        except Exception as e:
            logger.error(f"Error validating payroll {payroll_id}: {str(e)}")
            return False, f"Validation error: {str(e)}"
    
    def delete_payroll_safely(self, payroll_id, force_delete=False):
        """
        Safely delete a payroll record with all related data
        """
        try:
            # Validate deletion
            is_valid, result = self.validate_payroll_deletion(payroll_id)
            if not is_valid:
                self.deletion_stats['failed_deletions'] += 1
                return False, result
            
            if isinstance(result, dict):
                validation_info = result
            else:
                validation_info = {}
            
            # If not force delete and payroll is processed, ask for confirmation
            if validation_info.get('is_processed') and not force_delete:
                return False, "Payroll is processed. Use force_delete=True to proceed."
            
            payroll = Payroll.objects.get(id=payroll_id)
            employee_name = f"{payroll.employee.first_name} {payroll.employee.last_name}"
            period = f"{payroll.month} {payroll.year}"
            
            logger.info(f"Starting deletion of payroll ID {payroll_id} for {employee_name} - {period}")
            
            # Use database transaction for atomic deletion
            with transaction.atomic():
                deleted_records = {
                    'payroll_deductions': 0,
                    'salary_processing': 0,
                    'payroll_record': 0
                }
                
                # Step 1: Delete related PayrollDeduction records
                deduction_count = PayrollDeduction.objects.filter(payroll=payroll).delete()[0]
                deleted_records['payroll_deductions'] = deduction_count
                self.deletion_stats['related_records_cleaned'] += deduction_count
                logger.info(f"Deleted {deduction_count} payroll deduction records")
                
                # Step 2: Delete related SalaryProcessing records
                processing_count = SalaryProcessing.objects.filter(payroll_record=payroll).delete()[0]
                deleted_records['salary_processing'] = processing_count
                self.deletion_stats['related_records_cleaned'] += processing_count
                logger.info(f"Deleted {processing_count} salary processing records")
                
                # Step 3: Delete the main payroll record
                payroll.delete()
                deleted_records['payroll_record'] = 1
                self.deletion_stats['successful_deletions'] += 1
                logger.info(f"Successfully deleted payroll record for {employee_name}")
            
            # Log successful deletion
            logger.info(f"Deletion completed for payroll ID {payroll_id}: {deleted_records}")
            
            success_message = f"Successfully deleted payroll for {employee_name} ({period}). Related records: {sum(deleted_records.values()) - 1}"
            return True, success_message
            
        except Payroll.DoesNotExist:
            error_msg = f"Payroll record with ID {payroll_id} not found"
            self.deletion_stats['failed_deletions'] += 1
            logger.error(error_msg)
            return False, error_msg
            
        except Exception as e:
            error_msg = f"Error deleting payroll {payroll_id}: {str(e)}"
            self.deletion_stats['failed_deletions'] += 1
            logger.error(error_msg)
            return False, error_msg
    
    def find_and_delete_corrupted_payrolls(self):
        """
        Find and delete payroll records with corrupted JSON data
        """
        logger.info("Starting search for corrupted payroll records...")
        
        corrupted_records = []
        
        try:
            # Search for JSON-like patterns in payroll fields
            all_payrolls = Payroll.objects.all()
            
            for payroll in all_payrolls:
                if self.contains_json_data(payroll):
                    corrupted_records.append(payroll)
                    logger.warning(f"Found corrupted payroll ID {payroll.id}: {payroll.employee.first_name} {payroll.employee.last_name}")
            
            self.deletion_stats['json_records_found'] = len(corrupted_records)
            
            if not corrupted_records:
                logger.info("No corrupted payroll records found")
                return True, "No corrupted payroll records found"
            
            # Delete corrupted records
            deleted_count = 0
            for payroll in corrupted_records:
                success, message = self.delete_payroll_safely(payroll.id, force_delete=True)
                if success:
                    deleted_count += 1
                else:
                    logger.error(f"Failed to delete corrupted payroll {payroll.id}: {message}")
            
            result_message = f"Found {len(corrupted_records)} corrupted records, deleted {deleted_count} successfully"
            logger.info(result_message)
            return True, result_message
            
        except Exception as e:
            error_msg = f"Error scanning for corrupted payrolls: {str(e)}"
            logger.error(error_msg)
            return False, error_msg
    
    def contains_json_data(self, payroll):
        """
        Check if a payroll record contains JSON-like data
        """
        
        # Check text fields for JSON patterns
        text_fields = ['month', 'created_by']
        
        for field_name in text_fields:
            field_value = getattr(payroll, field_name, '')
            if field_value and self.is_json_like(str(field_value)):
                return True
        
        # Check all CharField and TextField values
        for field in payroll._meta.get_fields():
            if field.get_internal_type() in ['CharField', 'TextField']:
                field_value = getattr(payroll, field.name, '')
                if field_value and self.is_json_like(str(field_value)):
                    return True
        
        return False
    
    def is_json_like(self, value):
        """
        Check if a string value looks like JSON data
        """
        if not isinstance(value, str):
            return False
        
        # Remove whitespace
        value = value.strip()
        
        # Check for JSON-like patterns
        json_patterns = [
            r'^\{.*\}$',  # Objects: {...}
            r'^\[.*\]$',  # Arrays: [...]
            r'^\{.*\}.*\{.*\}$',  # Multiple objects
        ]
        
        for pattern in json_patterns:
            if re.match(pattern, value, re.DOTALL):
                try:
                    # Try to parse as JSON to confirm
                    json.loads(value)
                    return True
                except (json.JSONDecodeError, ValueError):
                    continue
        
        return False
    
    def get_deletion_statistics(self):
        """
        Get current deletion statistics
        """
        return self.deletion_stats
    
    def reset_statistics(self):
        """
        Reset deletion statistics
        """
        self.deletion_stats = {
            'total_processed': 0,
            'successful_deletions': 0,
            'failed_deletions': 0,
            'json_records_found': 0,
            'related_records_cleaned': 0
        }


def main():
    """
    Main function to demonstrate the enhanced payroll deletion system
    """
    print("Enhanced Payroll Deletion System")
    print("=" * 50)
    
    # Initialize the deletion system
    deletion_system = EnhancedPayrollDeletion()
    
    # Get current payroll count
    total_payrolls = Payroll.objects.count()
    print(f"Total payroll records in database: {total_payrolls}")
    
    if total_payrolls == 0:
        print("No payroll records found to delete.")
        return
    
    # Show available payroll records
    print("\nAvailable payroll records:")
    for payroll in Payroll.objects.all()[:5]:  # Show first 5
        print(f"  ID: {payroll.id} - {payroll.employee.first_name} {payroll.employee.last_name} - {payroll.month} {payroll.year}")
    
    if total_payrolls > 5:
        print(f"  ... and {total_payrolls - 5} more records")
    
    # Test validation
    print("\nTesting payroll validation...")
    test_payroll = Payroll.objects.first()
    if test_payroll:
        is_valid, result = deletion_system.validate_payroll_deletion(test_payroll.id)
        print(f"Validation result for payroll ID {test_payroll.id}: {'PASS' if is_valid else 'FAIL'}")
        if isinstance(result, dict):
            print(f"  Employee: {result['employee']}")
            print(f"  Period: {result['period']}")
            print(f"  Processed: {result['is_processed']}")
            print(f"  Related deductions: {result['related_deductions']}")
    
    # Test corrupted data search
    print("\nScanning for corrupted payroll records...")
    success, message = deletion_system.find_and_delete_corrupted_payrolls()
    print(f"Corrupted data scan: {'SUCCESS' if success else 'FAILED'}")
    print(f"Result: {message}")
    
    # Show final statistics
    stats = deletion_system.get_deletion_statistics()
    print(f"\nFinal Statistics:")
    print(f"  Total processed: {stats['total_processed']}")
    print(f"  Successful deletions: {stats['successful_deletions']}")
    print(f"  Failed deletions: {stats['failed_deletions']}")
    print(f"  JSON records found: {stats['json_records_found']}")
    print(f"  Related records cleaned: {stats['related_records_cleaned']}")
    
    print("\n" + "=" * 50)
    print("Enhanced Payroll Deletion System Test Completed!")


if __name__ == "__main__":
    main()