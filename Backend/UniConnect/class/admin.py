from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Class

class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'lecturer')
    search_fields = ('name', 'code', 'lecturer__username')
    list_filter = ('lecturer',)
    readonly_fields = ('display_students',)  # Only display this

    exclude = ('students',)  # Only show the class students

    def display_students(self, obj):
        students = obj.students.all()
        if not students:
            return "No students have joined."
        return "\n".join([f"{student.name}" for student in students])
    display_students.short_description = "Students Joined"

admin.site.register(Class, ClassAdmin)