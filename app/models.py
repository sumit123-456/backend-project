from django.db import models
from datetime import time



class HRProfile(models.Model):
    # ===== Personal Info =====
    full_name = models.CharField(max_length=200)
    employee_id = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    mobile = models.CharField(max_length=20)
    
    # ===== Official Info =====
    designation = models.CharField(max_length=100)
    department = models.CharField(max_length=100)
    date_of_joining = models.DateField()
    work_location = models.CharField(max_length=150)
    
    # ===== Credentials =====
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)
    access_level = models.CharField(max_length=50, default='HR')
    
    # ===== Profile Image =====
    profile_image = models.ImageField(upload_to='hr_profiles/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.employee_id})"
    

class Employee(models.Model):
    # -------------------------
    # BASIC DETAILS
    # -------------------------
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    address = models.TextField(blank=True, null=True)

    # -------------------------
    # FAMILY DETAILS (NEW)
    # -------------------------
    contact_number = models.CharField(max_length=20, blank=True, null=True)
    family_contact_number = models.CharField(max_length=20, blank=True, null=True)
    family_relation = models.CharField(max_length=50, blank=True, null=True)

    # -------------------------
    # EDUCATION DETAILS
    # -------------------------
    certifications = models.TextField(blank=True, null=True)

    # -------------------------
    # COMPANY OFFICIAL DETAILS
    # -------------------------
    company_id = models.CharField(max_length=50, unique=True)
    official_email = models.EmailField(blank=True, null=True)
    official_password = models.CharField(max_length=255, blank=True, null=True)

    designation = models.CharField(max_length=150)
    department = models.CharField(max_length=150)

    # -------------------------
    # EMPLOYEE IMAGE
    # -------------------------
    image = models.ImageField(upload_to="employees/", blank=True, null=True)

    # -------------------------
    # CONTRACT & PACKAGE
    # -------------------------
    package = models.DecimalField(max_digits=10, decimal_places=2)
    contract_years = models.IntegerField(default=1)
    contract_start_date = models.DateField(blank=True, null=True)
    contract_end_date = models.DateField(blank=True, null=True)

    resigned_date = models.DateTimeField(blank=True, null=True)


    # -------------------------
    # AUTO DATE FIELDS
    # -------------------------
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"






class TeamLeader(models.Model):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name="team_leader")

    # Extra TL fields
    experience_years = models.IntegerField()
    team_size = models.CharField(max_length=20)
    responsibilities = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"TL - {self.employee.first_name} {self.employee.last_name}"


class TeamAssignment(models.Model):
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    role = models.CharField(max_length=150)
    assignment_date = models.DateField()
    notes = models.TextField(blank=True, null=True)

    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.employee.first_name} assigned to {self.team_leader.employee.first_name}"

    
class ProjectAssignment(models.Model):
    project_name = models.CharField(max_length=200)
    project_code = models.CharField(max_length=100)
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE)
    team_members = models.ManyToManyField(Employee)
    priority = models.CharField(max_length=20)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name


# Removed duplicate Announcement model - using the enhanced version below
    


class Payroll(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)

    month = models.CharField(max_length=20)          # Example: "January 2025"
    year = models.PositiveIntegerField(default=2025)
    base_salary = models.DecimalField(max_digits=10, decimal_places=2)
    pf_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    professional_tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leave_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    late_arrival_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    half_day_deduction = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    other_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    allowances = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    overtime_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    final_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    created_by = models.CharField(max_length=200)    # HR Name
    created_at = models.DateTimeField(auto_now_add=True)
    is_processed = models.BooleanField(default=False)
    processed_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.month} {self.year}"


# ============================================================================
# NEW COMPREHENSIVE MODELS FOR HR SYSTEM
# ============================================================================

class Attendance(models.Model):
    """
    Comprehensive Attendance Model for tracking employee attendance
    """
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('half_day', 'Half Day'),
        ('leave', 'On Leave'),
        ('late', 'Late Arrival'),
        ('early_departure', 'Early Departure'),
        ('holiday', 'Holiday'),
        ('weekend', 'Weekend'),
        ('remote_work', 'Remote Work'),
    ]
    
    SHIFT_CHOICES = [
        ('morning', 'Morning Shift (9 AM - 6 PM)'),
        ('evening', 'Evening Shift (2 PM - 11 PM)'),
        ('night', 'Night Shift (11 PM - 8 AM)'),
        ('general', 'General Shift'),
        ('flexible', 'Flexible Timing'),
        ('full_time', 'Full Time'),
        ('part_time', 'Part Time'),
    ]
    
    # Employee relationship
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendances')
    
    # Date and Time fields
    attendance_date = models.DateField()
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    break_start_time = models.TimeField(null=True, blank=True)
    break_end_time = models.TimeField(null=True, blank=True)
    
    # Attendance tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='present')
    shift_type = models.CharField(max_length=20, choices=SHIFT_CHOICES, default='morning')
    
    # Work hours calculation
    total_worked_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    break_duration_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Location tracking
    check_in_location = models.CharField(max_length=255, null=True, blank=True)
    check_out_location = models.CharField(max_length=255, null=True, blank=True)
    device_info = models.TextField(null=True, blank=True)
    
    # Additional details
    remarks = models.TextField(null=True, blank=True)
    approved_by = models.CharField(max_length=200, null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    
    # Check-in/Check-out management fields
    is_check_in_allowed = models.BooleanField(default=True)  # Check if check-in is allowed (before 10:10 AM)
    can_check_out = models.BooleanField(default=False)      # Check if 8 hours completed for check-out
    check_in_reset_at = models.DateTimeField(null=True, blank=True)  # 24-hour reset time
    
    # Auto fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.attendance_date} - {self.status}"
    
    class Meta:
        ordering = ['-attendance_date']
        unique_together = ['employee', 'attendance_date']


class LeaveApply(models.Model):
    """
    Comprehensive Leave Application Model for employees
    """
    LEAVE_TYPE_CHOICES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('casual', 'Casual Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('emergency', 'Emergency Leave'),
        ('unpaid', 'Unpaid Leave'),
        ('half_day', 'Half Day Leave'),
        ('compensatory', 'Compensatory Off'),
        ('work_from_home', 'Work From Home'),
        ('bereavement', 'Bereavement Leave'),
        ('study', 'Study Leave'),
        ('marriage', 'Marriage Leave'),
        ('medical', 'Medical Leave'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
        ('revoked', 'Revoked'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Employee relationship
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_applications')
    
    # Leave details
    leave_type = models.CharField(max_length=30, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    total_days = models.PositiveIntegerField()
    half_day = models.BooleanField(default=False)
    half_day_session = models.CharField(max_length=20, null=True, blank=True, choices=[
        ('morning', 'Morning Session'),
        ('afternoon', 'Afternoon Session'),
    ])
    
    # Application details
    reason = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    contact_details = models.CharField(max_length=255, null=True, blank=True)
    emergency_contact = models.CharField(max_length=255, null=True, blank=True)
    
    # Supporting documents
    supporting_document = models.FileField(upload_to='leave_documents/', null=True, blank=True)
    medical_certificate = models.FileField(upload_to='leave_documents/', null=True, blank=True)
    
    # Approval workflow
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    applied_at = models.DateTimeField(auto_now_add=True)
    
    # Approval details
    approved_by = models.CharField(max_length=200, null=True, blank=True)
    approval_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)
    
    # Manager comments
    manager_comments = models.TextField(null=True, blank=True)
    hr_comments = models.TextField(null=True, blank=True)
    
    # Related TL approval (if applicable)
    tl_approved = models.BooleanField(default=False)
    tl_approved_by = models.CharField(max_length=200, null=True, blank=True)
    tl_approval_date = models.DateTimeField(null=True, blank=True)
    tl_comments = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.leave_type} ({self.start_date} to {self.end_date})"
    
    class Meta:
        ordering = ['-applied_at']


class LeaveApproval(models.Model):
    """
    Comprehensive Leave Approval Model for TLs and HRs
    """
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('modified', 'Modified'),
        ('escalated', 'Escalated'),
    ]
    
    APPROVER_TYPE_CHOICES = [
        ('team_leader', 'Team Leader'),
        ('hr', 'HR Manager'),
        ('senior_manager', 'Senior Manager'),
        ('director', 'Director'),
    ]
    
    DECISION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
        ('modify', 'Modify Request'),
        ('need_more_info', 'Need More Information'),
        ('escalate', 'Escalate to Higher Authority'),
    ]
    
    # Leave relationship
    leave_application = models.ForeignKey(LeaveApply, on_delete=models.CASCADE, related_name='approvals')
    
    # Approval workflow
    approver_type = models.CharField(max_length=20, choices=APPROVER_TYPE_CHOICES)
    approver_name = models.CharField(max_length=200)
    approver_email = models.EmailField()
    
    # Decision details
    decision = models.CharField(max_length=20, choices=DECISION_CHOICES)
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='pending')
    
    # Timing
    assigned_at = models.DateTimeField(auto_now_add=True)
    decision_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    
    # Comments and modifications
    comments = models.TextField(null=True, blank=True)
    modified_start_date = models.DateField(null=True, blank=True)
    modified_end_date = models.DateField(null=True, blank=True)
    modified_days = models.PositiveIntegerField(null=True, blank=True)
    modified_reason = models.TextField(null=True, blank=True)
    
    # Escalation details
    escalated_to = models.CharField(max_length=200, null=True, blank=True)
    escalation_reason = models.TextField(null=True, blank=True)
    escalated_date = models.DateTimeField(null=True, blank=True)
    
    # Notifications
    reminder_sent = models.BooleanField(default=False)
    last_reminder_date = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.leave_application.employee.first_name} - {self.approver_type} - {self.status}"
    
    class Meta:
        ordering = ['-assigned_at']


class Announcement(models.Model):
    """
    Enhanced Announcement Model for company-wide communications
    """
    CATEGORY_CHOICES = [
        ('company_news', 'Company News'),
        ('hr_updates', 'HR Updates'),
        ('policy_changes', 'Policy Changes'),
        ('events', 'Events'),
        ('general', 'General'),
        ('holiday', 'Holiday Notice'),
        ('training', 'Training & Development'),
        ('awards', 'Awards & Recognition'),
        ('technology', 'Technology Updates'),
        ('facilities', 'Facilities & Infrastructure'),
        ('safety', 'Safety & Security'),
        ('compliance', 'Compliance & Legal'),
        ('financial', 'Financial Updates'),
        ('product', 'Product Updates'),
        ('marketing', 'Marketing & Sales'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
        ('urgent', 'Urgent'),
    ]
    
    AUDIENCE_CHOICES = [
        ('all', 'All Employees'),
        ('management', 'Management Only'),
        ('department', 'Specific Departments'),
        ('location', 'Specific Locations'),
        ('contract_type', 'Contract Type Based'),
        ('role_based', 'Role Based'),
    ]
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('scheduled', 'Scheduled'),
        ('published', 'Published'),
        ('expired', 'Expired'),
        ('archived', 'Archived'),
        ('withdrawn', 'Withdrawn'),
    ]
    
    # Basic announcement details
    title = models.CharField(max_length=255)
    content = models.TextField()
    summary = models.TextField(null=True, blank=True)
    
    # Classification
    category = models.CharField(max_length=30, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='draft')
    
    # Target audience
    target_audience = models.CharField(max_length=30, choices=AUDIENCE_CHOICES, default='all')
    target_departments = models.JSONField(default=list, blank=True)
    target_locations = models.JSONField(default=list, blank=True)
    target_roles = models.JSONField(default=list, blank=True)
    
    # Scheduling
    publish_date = models.DateTimeField(null=True, blank=True)
    expiry_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Author details
    created_by = models.CharField(max_length=200)
    author_designation = models.CharField(max_length=200, null=True, blank=True)
    author_department = models.CharField(max_length=200, null=True, blank=True)
    
    # Attachments and media
    attachments = models.FileField(upload_to='announcement_attachments/', null=True, blank=True)
    image = models.ImageField(upload_to='announcement_images/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    
    # Social features
    likes_count = models.PositiveIntegerField(default=0)
    comments_enabled = models.BooleanField(default=True)
    shares_count = models.PositiveIntegerField(default=0)
    
    # Compliance and tracking
    compliance_required = models.BooleanField(default=False)
    acknowledgment_required = models.BooleanField(default=False)
    read_by_count = models.PositiveIntegerField(default=0)
    acknowledged_by_count = models.PositiveIntegerField(default=0)
    
    # SEO and search
    tags = models.JSONField(default=list, blank=True)
    keywords = models.CharField(max_length=500, null=True, blank=True)
    
    # Comments section
    comments = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.category} - {self.priority}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'priority']),
            models.Index(fields=['status', 'publish_date']),
            models.Index(fields=['expiry_date']),
        ]





class ProjectTask(models.Model):
    """
    Project Task Model for detailed task tracking within projects
    """
    TASK_STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('in_review', 'In Review'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
        ('cancelled', 'Cancelled'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    # Task relationships
    project = models.ForeignKey(ProjectAssignment, on_delete=models.CASCADE, related_name='tasks')
    assigned_to = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='assigned_tasks')
    assigned_by = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='assigned_tasks')
    
    # Task details
    title = models.CharField(max_length=255)
    description = models.TextField()
    task_status = models.CharField(max_length=20, choices=TASK_STATUS_CHOICES, default='not_started')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    
    # Timing
    created_at = models.DateTimeField(auto_now_add=True)
    start_date = models.DateTimeField()
    due_date = models.DateTimeField()
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Effort tracking
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    
    # Progress tracking
    progress_percentage = models.PositiveIntegerField(default=0)
    milestone = models.CharField(max_length=100, null=True, blank=True)
    
    # Quality and review
    quality_score = models.PositiveIntegerField(null=True, blank=True)
    reviewed_by = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='reviewed_tasks', null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - {self.project.project_name}"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'assigned_to']),
            models.Index(fields=['task_status', 'priority']),
            models.Index(fields=['due_date']),
        ]


class ProjectMilestone(models.Model):
    """
    Project Milestone Model for tracking project milestones and completion
    """
    STATUS_CHOICES = [
        ('planned', 'Planned'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('delayed', 'Delayed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Milestone relationships
    project = models.ForeignKey(ProjectAssignment, on_delete=models.CASCADE, related_name='milestones')
    
    # Milestone details
    title = models.CharField(max_length=255)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='planned')
    
    # Timing
    planned_date = models.DateField()
    actual_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Progress
    completion_percentage = models.PositiveIntegerField(default=0)
    deliverables = models.TextField(null=True, blank=True)
    
    # Team tracking
    responsible_employees = models.ManyToManyField(Employee, related_name='milestone_responsibilities')
    
    def __str__(self):
        return f"{self.title} - {self.project.project_name}"
    
    class Meta:
        ordering = ['planned_date']


# ============================================================================
# PROJECT DISCUSSION MODEL
# ============================================================================

class ProjectDiscussion(models.Model):
    """
    Project Discussion Model for project-related communications
    """
    MESSAGE_TYPE_CHOICES = [
        ('message', 'Message'),
        ('update', 'Project Update'),
        ('question', 'Question'),
        ('task_assignment', 'Task Assignment'),
        ('completion_report', 'Completion Report'),
        ('issue', 'Issue/Problem'),
        ('suggestion', 'Suggestion'),
        ('status_report', 'Status Report'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
        ('critical', 'Critical'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
        ('pending_review', 'Pending Review'),
        ('escalated', 'Escalated'),
    ]
    
    # Relationships
    project = models.ForeignKey(ProjectAssignment, on_delete=models.CASCADE, related_name='discussions')
    sender_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sent_messages')
    receiver_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='received_messages', null=True, blank=True)
    sender_tl = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='sent_tl_messages', null=True, blank=True)
    receiver_tl = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='received_tl_messages', null=True, blank=True)
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    
    # Message details
    message_type = models.CharField(max_length=20, choices=MESSAGE_TYPE_CHOICES, default='message')
    subject = models.CharField(max_length=255)
    content = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    is_announcement = models.BooleanField(default=False)
    
    # Attachments
    attachment = models.FileField(upload_to='project_discussions/', null=True, blank=True)
    attachment_name = models.CharField(max_length=255, null=True, blank=True)
    
    # Task-related fields
    task_due_date = models.DateTimeField(null=True, blank=True)
    task_status = models.CharField(max_length=50, null=True, blank=True)
    estimated_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    actual_hours = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    completion_percentage = models.PositiveIntegerField(default=0)
    milestone_reached = models.CharField(max_length=100, null=True, blank=True)
    
    # Tracking
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    read_at = models.DateTimeField(null=True, blank=True)
    resolved_by = models.CharField(max_length=200, null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.subject} - {self.project.project_name}"
    
    def get_sender_name(self):
        """Get the name of the message sender"""
        if self.sender_employee:
            return f"{self.sender_employee.first_name} {self.sender_employee.last_name}"
        elif self.sender_tl:
            return f"TL {self.sender_tl.employee.first_name} {self.sender_tl.employee.last_name}"
        return "Unknown Sender"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['project', 'created_at']),
            models.Index(fields=['sender_employee', 'created_at']),
            models.Index(fields=['sender_tl', 'created_at']),
            models.Index(fields=['status', 'priority']),
            models.Index(fields=['message_type']),
        ]


# ============================================================================
# ENHANCED PAYROLL & ATTENDANCE MANAGEMENT MODELS
# ============================================================================

class MonthlyAttendanceSummary(models.Model):
    """
    Monthly Attendance Summary for tracking monthly attendance statistics
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='monthly_attendance')
    
    # Month and Year
    month = models.CharField(max_length=20)  # Example: "January"
    year = models.PositiveIntegerField()
    
    # Attendance Statistics
    total_working_days = models.PositiveIntegerField(default=0)
    present_days = models.PositiveIntegerField(default=0)
    absent_days = models.PositiveIntegerField(default=0)
    half_days = models.PositiveIntegerField(default=0)
    late_arrivals = models.PositiveIntegerField(default=0)
    approved_leaves = models.PositiveIntegerField(default=0)
    unpaid_leaves = models.PositiveIntegerField(default=0)
    
    # Special Cases
    holiday_days = models.PositiveIntegerField(default=0)
    weekend_days = models.PositiveIntegerField(default=0)
    remote_work_days = models.PositiveIntegerField(default=0)
    
    # Hours tracking
    total_worked_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_overtime_hours = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    
    # Salary Calculation Fields
    salary_deduction_for_absences = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salary_deduction_for_half_days = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    salary_deduction_for_late_arrivals = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    leave_encashment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    is_finalized = models.BooleanField(default=False)
    finalized_by = models.CharField(max_length=200, null=True, blank=True)
    finalized_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.month} {self.year}"
    
    class Meta:
        unique_together = ['employee', 'month', 'year']
        ordering = ['-year', '-month']


class AttendanceApproval(models.Model):
    """
    Attendance Approval Model for TL approval workflow
    """
    APPROVAL_STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('modified', 'Modified'),
    ]
    
    # Relationships
    attendance = models.OneToOneField(Attendance, on_delete=models.CASCADE, related_name='approval')
    team_leader = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='attendance_approvals')
    
    # Approval details
    status = models.CharField(max_length=20, choices=APPROVAL_STATUS_CHOICES, default='pending')
    
    # Approval workflow
    requested_at = models.DateTimeField(auto_now_add=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)
    
    # Comments and modifications
    tl_comments = models.TextField(null=True, blank=True)
    modified_check_in_time = models.TimeField(null=True, blank=True)
    modified_check_out_time = models.TimeField(null=True, blank=True)
    
    # Late arrival handling
    is_late_arrival = models.BooleanField(default=False)
    late_minutes = models.PositiveIntegerField(default=0)
    marked_as_half_day = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Attendance Approval - {self.attendance.employee.first_name} - {self.attendance.attendance_date} - {self.status}"
    
    class Meta:
        ordering = ['-requested_at']


class PayrollDeduction(models.Model):
    """
    Payroll Deduction Model for detailed salary deductions
    """
    DEDUCTION_TYPE_CHOICES = [
        ('absent', 'Absence Deduction'),
        ('half_day', 'Half Day Deduction'),
        ('late_arrival', 'Late Arrival Deduction'),
        ('unpaid_leave', 'Unpaid Leave Deduction'),
        ('leave_without_pay', 'Leave Without Pay'),
        ('misconduct', 'Misconduct Deduction'),
        ('advance_salary', 'Advance Salary Recovery'),
        ('loan_recovery', 'Loan Recovery'),
        ('pf', 'Provident Fund'),
        ('professional_tax', 'Professional Tax'),
        ('other', 'Other Deductions'),
    ]
    
    # Relationships
    payroll = models.ForeignKey(Payroll, on_delete=models.CASCADE, related_name='deductions')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    # Deduction details
    deduction_type = models.CharField(max_length=30, choices=DEDUCTION_TYPE_CHOICES)
    description = models.TextField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Related records for tracking
    attendance_record = models.ForeignKey(Attendance, on_delete=models.CASCADE, null=True, blank=True)
    leave_application = models.ForeignKey(LeaveApply, on_delete=models.CASCADE, null=True, blank=True)
    monthly_summary = models.ForeignKey(MonthlyAttendanceSummary, on_delete=models.CASCADE, null=True, blank=True)
    
    # Calculation details
    calculation_basis = models.CharField(max_length=100, null=True, blank=True)  # e.g., "Per day salary", "Per hour rate"
    units_deducted = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)  # Days, hours, etc.
    
    # Status and tracking
    is_approved = models.BooleanField(default=True)
    approved_by = models.CharField(max_length=200, null=True, blank=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee.first_name} - {self.deduction_type} - ₹{self.amount}"
    
    class Meta:
        ordering = ['-created_at']


class SalaryProcessing(models.Model):
    """
    Salary Processing Model - Handle salary processing from 1st to 7th of month
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Employee relationship
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_processings')
    
    # Salary period
    salary_month = models.CharField(max_length=20)  # e.g., "November 2025"
    salary_year = models.PositiveIntegerField()
    
    # Processing details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    processing_start_date = models.DateField()  # 1st of month
    processing_end_date = models.DateField()    # 7th of month
    
    # Payroll calculations
    gross_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_deductions = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    net_salary = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Related records
    monthly_summary = models.ForeignKey(MonthlyAttendanceSummary, on_delete=models.CASCADE, null=True, blank=True)
    payroll_record = models.ForeignKey(Payroll, on_delete=models.CASCADE, null=True, blank=True)
    
    # Processing tracking
    processed_by = models.CharField(max_length=200, null=True, blank=True)
    processed_at = models.DateTimeField(null=True, blank=True)
    processed_date = models.DateField(null=True, blank=True)
    
    # Validation
    is_within_processing_window = models.BooleanField(default=False)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Salary Processing - {self.employee.first_name} {self.employee.last_name} - {self.salary_month} {self.salary_year}"
    
    class Meta:
        ordering = ['-salary_year', '-salary_month']
        unique_together = ['employee', 'salary_month', 'salary_year']


class AttendanceCheckLog(models.Model):
    """
    Attendance Check Log - Track all check-in/check-out activities with time restrictions
    """
    CHECK_TYPE_CHOICES = [
        ('check_in', 'Check In'),
        ('check_out', 'Check Out'),
        ('check_in_denied', 'Check In Denied'),
        ('check_out_denied', 'Check Out Denied'),
    ]
    
    DENIAL_REASON_CHOICES = [
        ('before_10_10_am', 'Check-in not allowed before 10:10 AM'),
        ('already_checked_in', 'Already checked in today'),
        ('already_checked_out', 'Already checked out today'),
        ('no_attendance_record', 'No attendance record found'),
        ('insufficient_hours', 'Insufficient worked hours for check-out'),
        ('weekend', 'Weekend - No check-in allowed'),
        ('holiday', 'Holiday - No check-in allowed'),
        ('other', 'Other reason'),
    ]
    
    # Employee relationship
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='check_logs')
    
    # Check details
    check_type = models.CharField(max_length=20, choices=CHECK_TYPE_CHOICES)
    check_time = models.DateTimeField()
    attendance_date = models.DateField()
    
    # Restriction info
    is_denied = models.BooleanField(default=False)
    denial_reason = models.CharField(max_length=50, choices=DENIAL_REASON_CHOICES, null=True, blank=True)
    denial_message = models.TextField(null=True, blank=True)
    
    # Additional tracking
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    device_info = models.CharField(max_length=255, null=True, blank=True)
    
    # Time calculations
    worked_hours_at_check = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    official_start_time = models.TimeField(default=time(10, 45))  # 10:45 AM - Late arrival after this
    check_in_allowed_time = models.TimeField(default=time(10, 0))   # 10:00 AM - Check-in starts
    check_in_end_time = models.TimeField(default=time(10, 50))     # 10:50 AM - Check-in ends
    check_out_start_time = models.TimeField(default=time(18, 20))  # 6:20 PM - Check-out starts
    check_out_end_time = models.TimeField(default=time(18, 45))    # 6:45 PM - Check-out ends
    required_work_hours = models.DecimalField(max_digits=4, decimal_places=2, default=8.0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.employee.first_name} {self.employee.last_name} - {self.check_type} - {self.check_time.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta:
        ordering = ['-check_time']


# ============================================================================
# NEW ATTENDANCE MODELS FOR ENHANCED SYSTEM
# ============================================================================

class PresentRecord(models.Model):
    """
    Present Record Model - Track employees marked as present with time
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='present_records')
    attendance_date = models.DateField()
    marked_time = models.DateTimeField(auto_now_add=True)
    check_in_time = models.TimeField(null=True, blank=True)
    check_out_time = models.TimeField(null=True, blank=True)
    
    # Additional tracking
    work_details = models.TextField(blank=True, null=True)
    late_marked = models.BooleanField(default=False)  # True if marked after 10:45 AM
    marked_by = models.CharField(max_length=200, null=True, blank=True)  # Self, HR, TL
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Present - {self.employee.first_name} {self.employee.last_name} - {self.attendance_date}"
    
    class Meta:
        unique_together = ['employee', 'attendance_date']
        ordering = ['-attendance_date']


class AbsentRecord(models.Model):
    """
    Absent Record Model - Track employees marked as absent with time
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='absent_records')
    attendance_date = models.DateField()
    marked_time = models.DateTimeField(auto_now_add=True)
    reason = models.TextField(blank=True, null=True)
    
    # Additional tracking
    marked_by = models.CharField(max_length=200, null=True, blank=True)  # Self, HR, TL
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=200, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Absent - {self.employee.first_name} {self.employee.last_name} - {self.attendance_date}"
    
    class Meta:
        unique_together = ['employee', 'attendance_date']
        ordering = ['-attendance_date']


class LateMarkRecord(models.Model):
    """
    Late Mark Record Model - Track employees marked late after 10:45 AM
    """
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='late_mark_records')
    attendance_date = models.DateField()
    marked_time = models.DateTimeField(auto_now_add=True)
    actual_check_in_time = models.TimeField()
    
    # Late arrival details
    late_minutes = models.PositiveIntegerField()  # How many minutes late
    reason = models.TextField(blank=True, null=True)
    
    # Additional tracking
    marked_by = models.CharField(max_length=200, null=True, blank=True)  # Self, HR, TL
    approved = models.BooleanField(default=False)
    approved_by = models.CharField(max_length=200, null=True, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Late Mark - {self.employee.first_name} {self.employee.last_name} - {self.attendance_date} ({self.late_minutes} min late)"
    
    class Meta:
        unique_together = ['employee', 'attendance_date']
        ordering = ['-attendance_date']


class DailyWorkCompletion(models.Model):
    """
    Daily Work Completion Model - Track work completion at office closing time (6:30 PM)
    """
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Work Completed'),
        ('partial', 'Partial Work'),
        ('not_completed', 'Not Completed'),
        ('extended', 'Extended Hours'),
    ]
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='daily_work_completions')
    work_date = models.DateField()
    office_closing_time = models.TimeField(default=time(18, 30))  # 6:30 PM
    
    # Work completion details
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    work_completion_time = models.DateTimeField(null=True, blank=True)
    
    # Work details submitted by employee
    tasks_completed = models.TextField()
    challenges_faced = models.TextField(blank=True, null=True)
    tomorrow_plan = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)
    
    # Time tracking
    actual_work_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    overtime_hours = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    
    # Approval workflow
    submitted_to_tl = models.BooleanField(default=False)
    tl_reviewed = models.BooleanField(default=False)
    tl_reviewed_by = models.CharField(max_length=200, null=True, blank=True)
    tl_reviewed_at = models.DateTimeField(null=True, blank=True)
    tl_comments = models.TextField(null=True, blank=True)
    
    submitted_to_hr = models.BooleanField(default=False)
    hr_reviewed = models.BooleanField(default=False)
    hr_reviewed_by = models.CharField(max_length=200, null=True, blank=True)
    hr_reviewed_at = models.DateTimeField(null=True, blank=True)
    hr_comments = models.TextField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Work Completion - {self.employee.first_name} {self.employee.last_name} - {self.work_date}"
    
    class Meta:
        unique_together = ['employee', 'work_date']
        ordering = ['-work_date']


# ============================================================================
# TEAM COMMUNICATION MODELS
# ============================================================================

class TeamChat(models.Model):
    """
    Team Chat Model for team communication between TL and team members
    """
    CHAT_TYPE_CHOICES = [
        ('direct', 'Direct Message'),
        ('team', 'Team Message'),
        ('group', 'Group Message'),
        ('announcement', 'Team Announcement'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('normal', 'Normal'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('closed', 'Closed'),
    ]
    
    # Relationships
    sender_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='sent_team_chats')
    sender_tl = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='sent_team_chats', null=True, blank=True)
    
    receiver_employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='received_team_chats', null=True, blank=True)
    receiver_tl = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='received_team_chats', null=True, blank=True)
    
    # Team relationship (for team messages)
    team_assignment = models.ForeignKey(TeamAssignment, on_delete=models.CASCADE, related_name='team_chats', null=True, blank=True)
    
    # Chat details
    chat_type = models.CharField(max_length=20, choices=CHAT_TYPE_CHOICES, default='direct')
    subject = models.CharField(max_length=255, blank=True, null=True)
    message = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='normal')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    
    # Thread support
    parent_message = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies', null=True, blank=True)
    
    # Attachments
    attachment = models.FileField(upload_to='team_chat_attachments/', null=True, blank=True)
    attachment_name = models.CharField(max_length=255, null=True, blank=True)
    
    # Read status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Reactions and engagement
    likes_count = models.PositiveIntegerField(default=0)
    replies_count = models.PositiveIntegerField(default=0)
    
    # Auto fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        sender_name = self.get_sender_name()
        if self.chat_type == 'direct':
            receiver_name = self.get_receiver_name()
            return f"Direct chat: {sender_name} → {receiver_name}"
        else:
            return f"Team chat: {sender_name} - {self.subject or self.message[:50]}"
    
    def get_sender_name(self):
        if self.sender_employee:
            return f"{self.sender_employee.first_name} {self.sender_employee.last_name}"
        elif self.sender_tl:
            return f"TL {self.sender_tl.employee.first_name} {self.sender_tl.employee.last_name}"
        return "Unknown Sender"
    
    def get_receiver_name(self):
        if self.receiver_employee:
            return f"{self.receiver_employee.first_name} {self.receiver_employee.last_name}"
        elif self.receiver_tl:
            return f"TL {self.receiver_tl.employee.first_name} {self.receiver_tl.employee.last_name}"
        return "Unknown Receiver"
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['chat_type', 'status']),
            models.Index(fields=['sender_employee', 'created_at']),
            models.Index(fields=['sender_tl', 'created_at']),
            models.Index(fields=['receiver_employee', 'created_at']),
            models.Index(fields=['receiver_tl', 'created_at']),
            models.Index(fields=['created_at']),
        ]


class ChatReaction(models.Model):
    """
    Chat Reaction Model for emoji reactions on team chat messages
    """
    REACTION_CHOICES = [
        ('like', '👍 Like'),
        ('love', '❤️ Love'),
        ('laugh', '😄 Laugh'),
        ('angry', '😠 Angry'),
        ('sad', '😢 Sad'),
        ('thumbs_up', '👍 Thumbs Up'),
        ('thumbs_down', '👎 Thumbs Down'),
        ('celebrate', '🎉 Celebrate'),
    ]
    
    # Relationships
    chat_message = models.ForeignKey(TeamChat, on_delete=models.CASCADE, related_name='reactions')
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='chat_reactions')
    tl = models.ForeignKey(TeamLeader, on_delete=models.CASCADE, related_name='chat_reactions', null=True, blank=True)
    
    # Reaction details
    reaction_type = models.CharField(max_length=20, choices=REACTION_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        reactor_name = self.get_reactor_name()
        return f"{reactor_name} reacted {self.get_reaction_emoji()} to chat message"
    
    def get_reactor_name(self):
        if self.employee:
            return f"{self.employee.first_name} {self.employee.last_name}"
        elif self.tl:
            return f"TL {self.tl.employee.first_name} {self.tl.employee.last_name}"
        return "Unknown User"
    
    def get_reaction_emoji(self):
        reaction_map = {
            'like': '👍',
            'love': '❤️',
            'laugh': '😄',
            'angry': '😠',
            'sad': '😢',
            'thumbs_up': '👍',
            'thumbs_down': '👎',
            'celebrate': '🎉',
        }
        return reaction_map.get(self.reaction_type, '👍')
    
    class Meta:
        unique_together = ['chat_message', 'employee', 'tl']
        ordering = ['-created_at']


class TeamChatSettings(models.Model):
    """
    Team Chat Settings for configuring team communication preferences
    """
    team_assignment = models.OneToOneField(TeamAssignment, on_delete=models.CASCADE, related_name='chat_settings')
    
    # Notification settings
    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=True)
    sound_notifications = models.BooleanField(default=True)
    
    # Privacy settings
    allow_direct_messages = models.BooleanField(default=True)
    auto_reply_enabled = models.BooleanField(default=False)
    auto_reply_message = models.TextField(blank=True, null=True)
    
    # Working hours
    working_hours_start = models.TimeField(default=time(9, 0))
    working_hours_end = models.TimeField(default=time(18, 0))
    working_days = models.JSONField(default=list)  # List of working days [0=Monday, 6=Sunday]
    
    # Auto-away settings
    auto_away_enabled = models.BooleanField(default=True)
    auto_away_minutes = models.PositiveIntegerField(default=30)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Chat Settings for {self.team_assignment.employee.first_name} {self.team_assignment.employee.last_name}"
    
    class Meta:
        verbose_name = 'Team Chat Settings'
        verbose_name_plural = 'Team Chat Settings'




