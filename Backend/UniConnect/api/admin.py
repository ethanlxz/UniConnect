from django.contrib import admin
from .models import StudentProfile, LecturerProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'username', 'name', 'email', 'contact_num']

@admin.register(LecturerProfile)
class LecturerProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'username', 'name', 'email', 'contact_num']