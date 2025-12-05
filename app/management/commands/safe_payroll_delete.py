import json
import re
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q
from django.contrib import messages
from app.models import Payroll, PayrollDeduction, SalaryProcessing, MonthlyAttendanceSummary


class Command(BaseCommand):
    help = 'Safely delete payroll records with comprehensive error handling and JSON data cleanup'

    def add_arguments(self, parser):
        parser.add_argument(
            '--payroll-id',
            type=int,
            help='Specific payroll ID to delete'
        )
        parser.add_argument(
            '--employee-id',
            type=int,
            help='Delete all payroll records for specific employee ID'
        )
        parser.add_argument(
            '--month',
            type=str,
            help='Delete payroll records for specific month (e.g., "November 2025")'
        )
        parser.add_argument(
            '--delete-corrupted',
            action='store_true',
            help='Delete payroll records containing corrupted JSON data'
        )
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be deleted without actually deleting'
        )
        parser.add_argument(
            '--force',
            action='store_true',
            help='Force deletion even for processed payrolls (use with caution)'
        )
        parser.add_argument(
            '--cleanup-all',
            action='store_true',
            help='Delete all payroll records (use with extreme caution)'
        )

    def handle(self, *args, **options):
        """Main command handler"""
        self.stdout.write(
            self.style.SUCCESS('Enhanced Payroll Deletion System Started')
        )
        
        # Initialize deletion system
        deletion_stats = {
            'total_processed': 0,
            'successful_deletions': 0,
            'failed_deletions': 0,
            'json_records_found': 0,
            'related_records_cleaned': 0
        }
        
        # Determine deletion scope
        payrolls_to_delete = self.get_payrolls_to_delete(options)
        
        if not payrolls_to_delete.exists():
            self.stdout.write(
                self.style.WARNING('No payroll records found matching the criteria')
            )
            return
        
        # Show what will be deleted
        self.show_deletion_preview(payrolls_to_delete, options)
        
        if options.get('dry_run'):
            self.stdout.write(
                self.style.SUCCESS('DRY RUN COMPLETED - No records were actually deleted')
            )
            return
        
        # Confirm deletion if not dry run
        if not self.confirm_deletion(options):
            self.stdout.write(self.style.ERROR('Operation cancelled by user'))
            return
        
        # Perform deletions
        self.perform_deletions(payrolls_to_delete, deletion_stats, options)
        
        # Show final results
        self.show_deletion_results(deletion_stats)

    def get_payrolls_to_delete(self, options):
        """Get payroll records based on deletion criteria"""
        payrolls = Payroll.objects.all()
        
        if options.get('payroll_id'):
            payrolls = payrolls.filter(id=options['payroll_id'])
        elif options.get('employee_id'):
            payrolls = payrolls.filter(employee_id=options['employee_id'])
        elif options.get('month'):
            payrolls = payrolls.filter(month=options['month'])
        elif options.get('delete_corrupted'):
            payrolls = self.get_corrupted_payrolls()
        elif options.get('cleanup_all'):
            # Show warning for cleanup all
            pass  # This will delete all payrolls
        else:
            # If no specific criteria, show help
            self.stdout.write(self.style.ERROR('Please specify deletion criteria'))
            self.stdout.write(self.style.WARNING('Use --help to see available options'))
            return Payroll.objects.none()
        
        return payrolls

    def get_corrupted_payrolls(self):
        """Find payroll records with corrupted JSON data"""
        corrupted_payrolls = []
        
        all_payrolls = Payroll.objects.all()
        
        for payroll in all_payrolls:
            if self.contains_json_data(payroll):
                corrupted_payrolls.append(payroll.id)
        
        return Payroll.objects.filter(id__in=corrupted_payrolls)

    def contains_json_data(self, payroll):
        """Check if a payroll record contains JSON-like data"""
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
        
        return False

    def show_deletion_preview(self, payrolls, options):
        """Show preview of what will be deleted"""
        self.stdout.write(
            self.style.WARNING(f'Found {payrolls.count()} payroll records to delete:')
        )
        
        for payroll in payrolls[:10]:  # Show first 10
            self.stdout.write(
                f'   ID: {payroll.id} | {payroll.employee.first_name} {payroll.employee.last_name} | '
                f'{payroll.month} {payroll.year} | Processed: {payroll.is_processed}'
            )
        
        if payrolls.count() > 10:
            self.stdout.write(f'   ... and {payrolls.count() - 10} more records')
        
        # Check for processed payrolls
        processed_count = payrolls.filter(is_processed=True).count()
        if processed_count > 0 and not options.get('force'):
            self.stdout.write(
                self.style.ERROR(f'WARNING: {processed_count} records are processed. Use --force to delete them.')
            )

    def confirm_deletion(self, options):
        """Get user confirmation for deletion"""
        if options.get('cleanup_all'):
            self.stdout.write(
                self.style.ERROR('DANGER: This will delete ALL payroll records!')
            )
            confirm = input('Type "DELETE ALL" to confirm: ')
            return confirm == 'DELETE ALL'
        elif options.get('delete_corrupted'):
            self.stdout.write(
                self.style.WARNING('This will delete all payroll records with corrupted JSON data.')
            )
            confirm = input('Type "DELETE CORRUPTED" to confirm: ')
            return confirm == 'DELETE CORRUPTED'
        else:
            confirm = input('Type "DELETE" to confirm deletion: ')
            return confirm == 'DELETE'

    @transaction.atomic
    def perform_deletions(self, payrolls, deletion_stats, options):
        """Perform the actual deletions"""
        self.stdout.write(self.style.SUCCESS('Starting deletions...'))
        
        for payroll in payrolls:
            try:
                deletion_stats['total_processed'] += 1
                
                # Validate deletion
                if payroll.is_processed and not options.get('force'):
                    self.stdout.write(
                        self.style.ERROR(f'Skipping processed payroll ID {payroll.id} (use --force)')
                    )
                    deletion_stats['failed_deletions'] += 1
                    continue
                
                employee_name = f"{payroll.employee.first_name} {payroll.employee.last_name}"
                period = f"{payroll.month} {payroll.year}"
                
                # Delete related records
                deduction_count = PayrollDeduction.objects.filter(payroll=payroll).delete()[0]
                processing_count = SalaryProcessing.objects.filter(payroll_record=payroll).delete()[0]
                
                deletion_stats['related_records_cleaned'] += deduction_count + processing_count
                
                # Delete the payroll record
                payroll.delete()
                
                deletion_stats['successful_deletions'] += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Deleted payroll for {employee_name} ({period})')
                )
                
            except Exception as e:
                deletion_stats['failed_deletions'] += 1
                self.stdout.write(
                    self.style.ERROR(f'Error deleting payroll ID {payroll.id}: {str(e)}')
                )

    def show_deletion_results(self, deletion_stats):
        """Show final deletion results"""
        self.stdout.write(self.style.SUCCESS('\nDELETION RESULTS'))
        self.stdout.write('=' * 40)
        self.stdout.write(f'Total processed: {deletion_stats["total_processed"]}')
        self.stdout.write(f'Successful deletions: {deletion_stats["successful_deletions"]}')
        self.stdout.write(f'Failed deletions: {deletion_stats["failed_deletions"]}')
        self.stdout.write(f'Related records cleaned: {deletion_stats["related_records_cleaned"]}')
        
        if deletion_stats['failed_deletions'] == 0:
            self.stdout.write(
                self.style.SUCCESS('All deletions completed successfully!')
            )
        else:
            self.stdout.write(
                self.style.WARNING(f'{deletion_stats["failed_deletions"]} deletions failed. Check logs for details.')
            )