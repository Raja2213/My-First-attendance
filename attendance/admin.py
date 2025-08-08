from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import Attendance
from .resources import AttendanceResource

@admin.register(Attendance)
class AttendanceAdmin(ImportExportModelAdmin):
    resource_class = AttendanceResource
    list_display = ('user', 'project_name', 'shift', 'date', 'time_in', 'time_out')
    list_filter = ('shift', 'date', 'project_name')
    search_fields = ('user__username', 'project_name')