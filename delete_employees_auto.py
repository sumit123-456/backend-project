#!/usr/bin/env python3
"""
Script to permanently delete specific employees from payroll system
Deletes: Bob Johnson, Jane Smith, John Doe (Non-interactive version)
"""

import os
import sys
import django

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'hrms.settings')
django.setup()

from app.models import (
    Employee, Payroll, MonthlyAttendanceSummary, Attendance,
    LeaveApply, AttendanceApproval, PayrollDeduction, SalaryProcessing,
    AttendanceCheckLog, ProjectAssignment, TeamAssignment, ProjectTask,
    ProjectDiscussion, ProjectMilestone
)

def print_separator(title):
    """Print a formatted separator"""
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}\n")

def find_employees_to_delete():
    """Find employees with the specified names"""
    employees_to_delete = []
    target_names = ['Bob Johnson', 'Jane Smith', 'John Doe']
    
    print_separator("SEARCHING FOR EMPLOYEES TO DELETE")
    
    for target_name in target_names:
        # Split name to search by first and last name
        name_parts = target_name.split()
        if len(name_parts) >= 2:
            first_name = name_parts[0]
            last_name = ' '.join(name_parts[1:])
            
            # Search for employees matching the name
            employees = Employee.objects.filter(
                first_name__iexact=first_name,
                last_name__iexact=last_name
            )
            
            print(f"Searching for '{target_name}':")
            print(f"  First name: '{first_name}', Last name: '{last_name}'")
            print(f"  Found {employees.count()} matching employees")
            
            for emp in employees:
                employees_to_delete.append(emp)
                print(f"  FOUND: {emp.first_name} {emp.last_name} (ID: {emp.id}, Email: {emp.email})")
        
        print()
    
    return employees_to_delete

def get_related_data_count(employee):
    """Count all related data for an employee"""
    counts = {}
    
    # Payroll records
    counts['payroll'] = Payroll.objects.filter(employee=employee).count()
    
    # Attendance records
    counts['attendance'] = Attendance.objects.filter(employee=employee).count()
    
    # Monthly attendance summaries
    counts['monthly_attendance'] = MonthlyAttendanceSummary.objects.filter(employee=employee).count()
    
    # Leave applications
    counts['leave_applications'] = LeaveApply.objects.filter(employee=employee).count()
    
    # Attendance approvals
    counts['attendance_approval'] = AttendanceApproval.objects.filter(attendance__employee=employee).count()
    
    # Payroll deductions
    counts['payroll_deductions'] = PayrollDeduction.objects.filter(employee=employee).count()
    
    # Salary processing
    counts['salary_processing'] = SalaryProcessing.objects.filter(employee=employee).count()
    
    # Check logs
    counts['check_logs'] = AttendanceCheckLog.objects.filter(employee=employee).count()
    
    # Project assignments
    counts['project_assignments'] = ProjectAssignment.objects.filter(team_members=employee).count()
    
    # Team assignments
    counts['team_assignments'] = TeamAssignment.objects.filter(employee=employee).count()
    
    # Project tasks
    counts['project_tasks'] = ProjectTask.objects.filter(assigned_to=employee).count()
    
    # Project discussions
    counts['project_discussions_sent'] = ProjectDiscussion.objects.filter(sender_employee=employee).count()
    counts['project_discussions_received'] = ProjectDiscussion.objects.filter(receiver_employee=employee).count()
    
    # Project milestones
    counts['project_milestones'] = ProjectMilestone.objects.filter(responsible_employees=employee).count()
    
    return counts

def delete_employee_data(employee):
    """Delete all data related to an employee"""
    print(f"\nDELETING ALL DATA FOR: {employee.first_name} {employee.last_name}")
    
    # Get counts before deletion
    counts = get_related_data_count(employee)
    
    print("Data to be deleted:")
    for data_type, count in counts.items():
        if count > 0:
            print(f"  - {data_type.replace('_', ' ').title()}: {count} records")
    
    total_records = sum(counts.values())
    print(f"\nTotal records to delete: {total_records}")
    
    if total_records == 0:
        print("No related data found. Proceeding with employee deletion only.")
    else:
        print("WARNING: This will permanently delete all related data!")
    
    try:
        # Delete in order to handle foreign key constraints
        print("\nDeleting related data...")
        
        # 1. Project discussions (both sent and received)
        if counts['project_discussions_sent'] > 0:
            deleted = ProjectDiscussion.objects.filter(sender_employee=employee).delete()[0]
            print(f"  Deleted {deleted} sent project discussions")
        
        if counts['project_discussions_received'] > 0:
            deleted = ProjectDiscussion.objects.filter(receiver_employee=employee).delete()[0]
            print(f"  Deleted {deleted} received project discussions")
        
        # 2. Project tasks
        if counts['project_tasks'] > 0:
            deleted = ProjectTask.objects.filter(assigned_to=employee).delete()[0]
            print(f"  Deleted {deleted} project tasks")
        
        # 3. Project milestones
        if counts['project_milestones'] > 0:
            deleted = ProjectMilestone.objects.filter(responsible_employees=employee).delete()[0]
            print(f"  Deleted {deleted} project milestone assignments")
        
        # 4. Project assignments (remove from team members)
        if counts['project_assignments'] > 0:
            projects = ProjectAssignment.objects.filter(team_members=employee)
            for project in projects:
                project.team_members.remove(employee)
            print(f"  Removed {employee.first_name} from {counts['project_assignments']} project assignments")
        
        # 5. Team assignments
        if counts['team_assignments'] > 0:
            deleted = TeamAssignment.objects.filter(employee=employee).delete()[0]
            print(f"  Deleted {deleted} team assignments")
        
        # 6. Attendance approvals
        if counts['attendance_approval'] > 0:
            deleted = AttendanceApproval.objects.filter(attendance__employee=employee).delete()[0]
            print(f"  Deleted {counts['attendance_approval']} attendance approvals")
        
        # 7. Check logs
        if counts['check_logs'] > 0:
            deleted = AttendanceCheckLog.objects.filter(employee=employee).delete()[0]
            print(f"  Deleted {deleted} check logs")
        
        # 8. Leave applications
        if counts['leave_applications'] > 0:
            deleted = LeaveApply.objects.filter(employee=employee).delete()[0]
            print(f"  Deleted {deleted} leave applications")
        
        # 9. Payroll deductions
        if counts['payroll_deductions'] > 0:
            deleted = PayrollDeduction.objects.filter(employee=employee).delete()[0]
            print(f"  Deleted {deleted} payroll deductions")
        
        # 10. Salary processing
        if counts['salary_processing'] > 0:
            deleted = SalaryProcessing.objects.filter(employee=employee).delete()[0]
            print(f"  Deleted {deleted} salary processing records")
        
        # 11. Monthly attendance summaries
        if counts['monthly_attendance'] > 0:
            deleted = MonthlyAttendanceSummary.objects.filter(employee=employee).delete()[0]
            print(f"  Deleted {deleted} monthly attendance summaries")
        
        # 12. Attendance records
        if counts['attendance'] > 0:
            deleted = Attendance.objects.filter(employee=employee).delete()[0]
            print(f"  Deleted {deleted} attendance records")
        
        # 13. Payroll records
        if counts['payroll'] > 0:
            deleted = Payroll.objects.filter(employee=employee).delete()[0]
            print(f"  Deleted {deleted} payroll records")
        
        # 14. Finally, delete the employee
        employee_name = f"{employee.first_name} {employee.last_name}"
        employee.delete()
        print(f"  Deleted employee record: {employee_name}")
        
        print(f"\nSuccessfully deleted all data for {employee_name}")
        return True
        
    except Exception as e:
        print(f"\nError deleting data for {employee.first_name} {employee.last_name}: {str(e)}")
        return False

def main():
    """Main function to delete employees"""
    print_separator("PERMANENT EMPLOYEE DELETION FROM PAYROLL SYSTEM")
    print("This script will permanently delete the following employees from the HR system:")
    print("- Bob Johnson")
    print("- Jane Smith")
    print("- John Doe")
    print("\nWARNING: This action cannot be undone!")
    
    # Find employees to delete
    employees_to_delete = find_employees_to_delete()
    
    if not employees_to_delete:
        print("\nNo employees found with the specified names.")
        print("Nothing to delete.")
        return
    
    print(f"\nSUMMARY:")
    print(f"Found {len(employees_to_delete)} employee(s) to delete:")
    for emp in employees_to_delete:
        print(f"  - {emp.first_name} {emp.last_name} (ID: {emp.id})")
    
    # Confirm bulk deletion
    print(f"\nWARNING: This will permanently delete ALL data for these {len(employees_to_delete)} employee(s)")
    print("including payroll, attendance, leave records, and all related data.")
    print("Auto-confirming deletion...")
    
    # Delete each employee
    successful_deletions = 0
    failed_deletions = 0
    
    for employee in employees_to_delete:
        if delete_employee_data(employee):
            successful_deletions += 1
        else:
            failed_deletions += 1
    
    # Final summary
    print_separator("DELETION SUMMARY")
    print(f"Successfully deleted: {successful_deletions} employee(s)")
    print(f"Failed deletions: {failed_deletions} employee(s)")
    
    if successful_deletions > 0:
        print(f"\nThe following employees have been permanently removed from the system:")
        for emp in employees_to_delete:
            if not hasattr(emp, 'pk') or emp.pk is None:
                print(f"  - {emp.first_name} {emp.last_name}")
    
    print(f"\nVerify deletion by checking the HR module - dummy data should no longer appear.")

if __name__ == "__main__":
    main()