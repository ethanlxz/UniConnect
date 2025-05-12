from django.db import models

class StudentProfile(models.Model):
    id = models.AutoField(primary_key=True)
	username =models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    age = models.IntegerField()
    contact_num = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username

class LecturerProfile(models.Model):
    id = models.AutoField(primary_key=True)
	username =models.CharField(max_length=30)
    name = models.CharField(max_length=30)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    contact_num = models.CharField(max_length=15, unique=True)

    def __str__(self):
        return self.username

class OTP_profile(models.Model):
	email = models.Emailfield()
	code = models.CharField(max_length=6)
	expriarationDate = models.DateTimeField(null=True, blank=True)

	def __str__(self):
        return self.email
