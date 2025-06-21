from django.db import models
from api.models import StudentProfile
from classing.models import Class

# Create your models here.
class Group(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_groups')
    members = models.ManyToManyField(StudentProfile, related_name='groups')
    is_finalized = models.BooleanField(default=False)

    def current_member_count(self):
        return self.members.count()

    def check_and_finalize(self):
        if self.current_member_count() >= self.class_instance.min_group_members:
            self.is_finalized = True
            self.save()

class GroupRequest(models.Model):
    sender = models.ForeignKey(StudentProfile, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(StudentProfile, related_name='received_requests', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.username} → {self.receiver.username}"

class TemporaryGroup(models.Model):
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='temp_groups')
    members = models.ManyToManyField(StudentProfile, related_name='temp_groups', blank=True)
    leader = models.ForeignKey(StudentProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='led_temp_groups')

    def current_member_count(self):
        return self.members.count()

    def is_available(self):
        return self.current_member_count() == 0

    def __str__(self):
        return f"TempGroup {self.id} ({self.class_instance.code})"