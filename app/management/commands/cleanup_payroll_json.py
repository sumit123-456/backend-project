import json
import re
from django.core.management.base import BaseCommand
from django.db.models import Q
from app.models import Payroll, PayrollDeduction, SalaryProcessing


class Command(BaseCommand):
    help = 'Clean up JSON data from payroll tables'

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete',
            action='store_true',
            help='Actually delete records (without this flag, only shows what would be deleted)',
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting (default behavior)',
        )

    def handle(self, *args, **options):
        delete_mode = options.get('delete', False)
        dry_run = options.get('dry_run', True) if not delete_mode else False
        
        if delete_mode:
            self.stdout.write(
                self.style.WARNING('WARNING: DELETE MODE: Records will be permanently removed!')
            )
            confirm = input('Type "DELETE" to confirm: ')
            if confirm != 'DELETE':
                self.stdout.write(self.style.ERROR('Operation cancelled.'))
                return
        
        # Find payroll records with JSON-like data
        json_payrolls = self.find_json_payroll_records()
        
        if not json_payrolls:
            self.stdout.write(
                self.style.SUCCESS('SUCCESS: No payroll records with JSON data found.')
            )
            return
        
        self.stdout.write(
            self.style.WARNING(f'Found {len(json_payrolls)} payroll records with JSON data:')
        )
        
        # Display details of records with JSON data
        for payroll in json_payrolls:
            self.stdout.write(f"\nINFO: Payroll Record ID: {payroll.id}")
            self.stdout.write(f"   Employee: {payroll.employee.first_name} {payroll.employee.last_name}")
            self.stdout.write(f"   Period: {payroll.month} {payroll.year}")
            self.stdout.write(f"   JSON Data Found In Fields:")
            
            json_fields = self.find_json_in_payroll_fields(payroll)
            for field_name, json_content in json_fields.items():
                self.stdout.write(f"     - {field_name}: {json_content[:100]}...")
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f"\nINFO: DRY RUN: Found {len(json_payrolls)} records to delete.")
            )
            self.stdout.write("   Use --delete flag to actually remove these records.")
            return
        
        # Delete the records
        deleted_count = 0
        for payroll in json_payrolls:
            try:
                # Delete related payroll deductions first
                PayrollDeduction.objects.filter(payroll=payroll).delete()
                
                # Delete related salary processing records
                SalaryProcessing.objects.filter(payroll_record=payroll).delete()
                
                # Delete the payroll record
                payroll.delete()
                deleted_count += 1
                
                self.stdout.write(
                    self.style.SUCCESS(f"SUCCESS: Deleted payroll record {payroll.id}")
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f"ERROR: Error deleting payroll {payroll.id}: {str(e)}")
                )
        
        self.stdout.write(
            self.style.SUCCESS(f"\nINFO: Cleanup completed: {deleted_count} payroll records deleted.")
        )

    def find_json_payroll_records(self):
        """Find payroll records that contain JSON-like data in their fields"""
        json_payrolls = []
        
        # Get all payroll records
        all_payrolls = Payroll.objects.all()
        
        for payroll in all_payrolls:
            if self.has_json_data(payroll):
                json_payrolls.append(payroll)
        
        return json_payrolls

    def has_json_data(self, payroll):
        """Check if a payroll record contains JSON-like data"""
        json_fields = self.find_json_in_payroll_fields(payroll)
        return len(json_fields) > 0

    def find_json_in_payroll_fields(self, payroll):
        """Find which fields in a payroll record contain JSON data"""
        json_fields = {}
        
        # List of text-based fields to check
        text_fields = ['month', 'created_by']
        
        for field_name in text_fields:
            field_value = getattr(payroll, field_name)
            if field_value and self.is_json_like(field_value):
                json_fields[field_name] = field_value
        
        # Check all CharField and TextField values
        for field in payroll._meta.get_fields():
            if field.get_internal_type() in ['CharField', 'TextField']:
                field_value = getattr(payroll, field.name)
                if field_value and self.is_json_like(str(field_value)):
                    json_fields[field.name] = str(field_value)
        
        return json_fields

    def is_json_like(self, value):
        """Check if a string value looks like JSON data"""
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
        
        # Check for JSON-like structure indicators
        json_indicators = ['{', '}', '[', ']', ':', ',']
        if all(indicator in value for indicator in json_indicators[:4]):
            return True
        
        return False