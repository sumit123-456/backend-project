from django.contrib import admin
from .models import (
    Employee,
    TeamLeader,
    TeamAssignment,
    ProjectAssignment,
    Announcement
)

admin.site.register(Employee)
admin.site.register(TeamLeader)
admin.site.register(TeamAssignment)
admin.site.register(ProjectAssignment)
admin.site.register(Announcement)
