from django.urls import path, include
from . import views

urlpatterns = [

    #----------------------------------------------------------------------------------
    
    ########################### Role Based Access Control URLs #########################
     path('', views.login_view, name='login'),
     path('logout/', views.logout_view, name='logout'),
     path('logout-confirmation/', views.logout_confirmation, name='logout_confirmation'),
    ###################### Dashboard URLs ###############################
     path('dashboard/', views.hr_dashboard, name='hr-dashboard'),
     path('employee-dashboard/', views.employee_dashboard, name='employee-dashboard'),
    #  -------------------------------------------------------------------------------------
    ################################ Employee Module URLs ################################
     path('employee-attendance/', views.employee_attendance, name='employee-attendance'),
     path('employee-attendance-records/', views.employee_attendance_records_simple, name='employee-attendance-records'),
     path('apply-leave/', views.employee_apply_leave, name='apply-leave'),
     path('payslip/', views.employee_payslip, name='payslip'),
     path('employee-profile/', views.employee_profile, name='employee-profile'),
     path('employee-project-dashboard/', views.employee_project_dashboard, name='employee-project-dashboard'),

     path('hr-profile/', views.hr_profile, name='hr-profile'),
     path('tl-profile/', views.tl_profile, name='tl-profile'),
     path('employee-attendance-page/', views.employee_attendance_page, name='employee-attendance-page'),
     path('hr-attendance-page/', views.hr_attendance_page, name='hr-attendance-page'),

    ################################ End Employee Module Url #############################
    # ----------------------------------------------------------------------------------------
    ################################ TL Modules Urls #####################################
     path('tl-dashboard/', views.tl_dashboard, name='tl-dashboard'),
     path('tl-reports/', views.tl_reports, name='tl-reports'),
     path('team-attendence/',views.tl_attendance, name='team-attendence'),
     path('team-leave-approval/', views.team_leave_approval, name='team-leave-approval'),
     path('tl-manage-team/', views.tl_manage_team, name='tl-manage-team'),
     path('tl-project-dashboard/', views.tl_project_dashboard, name='tl-project-dashboard'),
     path('tl-project-discussions/', views.tl_project_discussions, name='tl-project-discussions'),
     path('employee-project-discussions/', views.employee_project_discussions, name='employee-project-discussions'),
     path('send-project-message/', views.send_project_message, name='send-project-message'),
     path('get-project-discussions/', views.get_project_discussions, name='get-project-discussions'),

    
    ################################ TL Module Urls End ###################################
    


     path('employee/', views.employee , name='employee-management'),
     path("export-employees/", views.export_employees, name="export-employees"),
     path("show-all-employee/", views.show_all_employees, name="show-all-employee"),
     path("get-employee/<int:emp_id>/", views.get_employee, name="get_employee"),   
     path("delete-employee/<int:emp_id>/", views.delete_employee, name="delete-employee"),
     path("team/", views.team_page, name="team-page"),                     
     path("create-team-leader/", views.create_team_leader, name="create-tl"),
     path("assign-member-page/", views.assign_member_page, name="assign-member-page"),
     path("assign-member-submit/", views.assign_member_submit, name="assign-member-submit"),
     path("update-team-member/", views.tl_manage_team, name="update-team-member"),
     # path("remove-team-member/", views.remove_team_member, name="remove-team-member"),  # Function not implemented
     path("assign-project-page/", views.assign_project_page, name="assign-project-page"),
     path("assign-project-submit/", views.assign_project_submit, name="assign-project-submit"),
     path("get-team-members/", views.get_team_members, name="get-team-members"),
     path('team-info/', views.team_table, name='team-info'),
     path("team-leader/details/<int:tl_id>/", views.get_team_leader_details, name="tl-details"),
     path("delete-team-leader/<int:tl_id>/", views.delete_team_leader, name="delete-tl"),
     

     ############################## HR Management Urls ##########################################
    

     path('attendance/', views.hr_attendance_simple , name='attendance'),
     path('hr-attendance/', views.hr_attendance_simple , name='hr-attendance'),
     path('leave-approvals/', views.leave_approvals, name='leave-approvals'),

     ############################## Employee Payroll MAnagement Urls ##############################

     path('payroll/', views.payroll, name='payroll-management'),
     path("payroll-records/", views.payroll_records, name="payroll-records"),
     path("export-payroll/", views.export_payroll, name="export-payroll"),
     path("delete-payroll/", views.delete_payroll, name="delete-payroll"),   

     path('reports/', views.reports, name='hr-reports'),
     path("api/payroll-data/", views.get_payroll_data, name="payroll-data"),
     path('announcements/', views.announcements, name='hr-announcements'),
     
     # Announcement Management URLs
     path('announcements/view/<int:announcement_id>/', views.view_announcement, name='view-announcement'),
     path('announcements/edit/<int:announcement_id>/', views.edit_announcement_view, name='edit-announcement'),
     path('announcements/update/<int:announcement_id>/', views.update_announcement, name='update-announcement'),
     path('announcements/delete/<int:announcement_id>/', views.delete_announcement, name='delete-announcement'),
     
     # path('team/', views.team, name='hr-team'), # Commented out duplicate


     ######################################## HR Management URLs ####################
     path('create-hr/', views.hr_create, name='create-hr'),
     path('hr-list/', views.hr_list, name='hr-list'),
     path('delete-hr/<int:hr_id>/', views.delete_hr, name='delete-hr'),
     
     # Test leave management system
     path('test-leave-system/', views.test_leave_system, name='test-leave-system'),

    # ============================================================================
    # NEW PAYROLL & ATTENDANCE MANAGEMENT URLs
    # ============================================================================

    # Employee Attendance URLs
    path('employee-check-in/', views.employee_attendance_simple, name='employee-check-in'),
    path('employee-check-out/', views.employee_check_out, name='employee-check-out'),

    # Team Leader Attendance Management URLs
    path('tl-attendance-management/', views.tl_attendance_management, name='tl-attendance-management'),

    # HR Monthly Attendance Summary URLs
    path('hr-monthly-attendance-summary/', views.hr_monthly_attendance_summary, name='hr-monthly-attendance-summary'),

    # HR Payroll Calculations URLs
    path('hr-payroll-calculations/', views.hr_payroll_calculations, name='hr-payroll-calculations'),


    path('payroll-emp/', views.payrollemployeepage, name='payroll-emp'),
    # ============================================================================
    # TEAM CHAT URLS
    # ============================================================================
    
    # Main chat dashboard
    path('team-chat/', views.team_chat_dashboard, name='team-chat'),
    
    # Chat API endpoints
    path('send-team-message/', views.send_team_message, name='send-team-message'),
    path('get-conversations/', views.get_conversations, name='get-conversations'),
    path('mark-messages-read/', views.mark_messages_read, name='mark-messages-read'),
    path('chat-reaction/', views.chat_reaction, name='chat-reaction'),
    path('get-unread-count/', views.get_unread_count, name='get-unread-count'),
    path('chat-search/', views.chat_search, name='chat-search'),
    
    # ============================================================================
    # ENHANCED ATTENDANCE SYSTEM URLS
    # ============================================================================
    
    # Employee Enhanced Attendance
    path('enhanced-attendance/', views.enhanced_attendance_dashboard, name='enhanced-attendance'),
    path('mark-present-today/', views.mark_present_today, name='mark-present-today'),
    path('mark-absent-today/', views.mark_absent_today, name='mark-absent-today'),
    path('work-complete-today/', views.work_complete_today, name='work-complete-today'),
    path('attendance-table/', views.attendance_table_view, name='attendance-table'),
    
    # Date-specific attendance marking
    path('mark-present-date/', views.mark_present_date, name='mark-present-date'),
    path('mark-absent-date/', views.mark_absent_date, name='mark-absent-date'),
    path('get-attendance-calendar/', views.get_attendance_calendar, name='get-attendance-calendar'),
    
    # HR Enhanced Attendance Management
    path('hr-enhanced-attendance/', views.hr_enhanced_attendance_view, name='hr-enhanced-attendance'),
    
    # TL Enhanced Attendance Management
    path('tl-enhanced-attendance/', views.tl_enhanced_attendance_view, name='tl-enhanced-attendance'),
    
    #  -------------------------------------------------------------------------------------------
    ################################## Team Lead Management URLs ####################################
    # --------------------------------------------------------------------------------------------



]
