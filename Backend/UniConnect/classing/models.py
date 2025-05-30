from django.db import models
from api.utils import generate_random_code
from api.models import LecturerProfile, StudentProfile

# Create your models here.
class Class(models.Model):
    class_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=6, unique=True, blank=True)
    lecturer = models.ForeignKey(LecturerProfile, on_delete=models.CASCADE, related_name='classes')
    students = models.ManyToManyField(StudentProfile, blank=True, related_name='joined_classes')
    max_students = models.PositiveIntegerField()
    group = models.PositiveIntegerField(default=1)
    min_group_members = models.PositiveIntegerField(default=1)

    def current_student_count(self):
        return self.students.count()

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = generate_random_code()
            while Class.objects.filter(code=self.code).exists():  # Check for uniqueness
                self.code = generate_random_code()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.code})"