from django.db import models

class StudentProfile(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    contact_num = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name

class LecturerProfile(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=50)
    contact_num = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.name