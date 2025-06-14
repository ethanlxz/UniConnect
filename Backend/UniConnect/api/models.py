from django.db import models

class StudentProfile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    contact_num = models.CharField(max_length=15, unique=True)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    major = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='student_profile_image/', default='default.jpg')
    bio = models.TextField(max_length=200, default='Bio loading… please wait.')
    instagram_id = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.username

class LecturerProfile(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    contact_num = models.CharField(max_length=15, unique=True)
    major = models.CharField(max_length=50)
    profile_image = models.ImageField(upload_to='lecturer_profile_image/', default='default.jpg')

    def __str__(self):
        return self.username

class OTP_profile(models.Model):
    email = models.EmailField()
    code = models.CharField(max_length=6)
    expriarationDate = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.email
