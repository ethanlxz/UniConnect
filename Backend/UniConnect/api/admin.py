from django.contrib import admin

# Register your models here.
from .models import StudentProfile, LecturerProfile

admin.site.register(StudentProfile)
admin.site.register(LecturerProfile)