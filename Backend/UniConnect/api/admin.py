from django.contrib import admin
from django.contrib.auth.hashers import make_password
from .models import StudentProfile, LecturerProfile

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'username', 'name', 'email', 'contact_num', 'gender', 'major']
    
    def save_model(self, request, obj, form, change):
        # If password is being set/updated
        if 'password' in form.changed_data:
            # Hash the password only if it's not already hashed
            if not obj.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')):
                obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)

@admin.register(LecturerProfile)
class LecturerProfileAdmin(admin.ModelAdmin):
    readonly_fields = ['id']
    list_display = ['id', 'username', 'name', 'email', 'contact_num', 'major']
    
    def save_model(self, request, obj, form, change):
        # If password is being set/updated
        if 'password' in form.changed_data:
            # Hash the password only if it's not already hashed
            if not obj.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2$')):
                obj.password = make_password(obj.password)
        super().save_model(request, obj, form, change)