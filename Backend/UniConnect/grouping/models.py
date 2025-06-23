from django.db import models
from api.models import StudentProfile
from classing.models import Class

# Create your models here.

class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    class_instance = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='class_groups')
    max_members = models.PositiveIntegerField(help_text="Exact number of members required in this group")
    members = models.ManyToManyField(StudentProfile, related_name='groups')
    leader = models.ForeignKey(StudentProfile, null=True, blank=True, on_delete=models.SET_NULL, related_name='led_groups')
    is_full = models.BooleanField(default=False, editable=False)

    def current_member_count(self):
        return self.members.count()

    def update_is_full(self):
        self.is_full = (self.current_member_count() >= self.max_members)
        self.save(update_fields=['is_full'])

    def __str__(self):
        return f"Group {self.group_id} (Class: {self.class_instance})"

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
    is_finalized = models.BooleanField(default=False, editable=False)

    def current_member_count(self):
        return self.members.count()

    def is_available(self):
        return self.current_member_count() == 0

    def __str__(self):
        return f"TempGroup {self.id} ({self.class_instance.code})"
    
class JoinGroupRequest(models.Model):
    sender = models.ForeignKey(StudentProfile, related_name='join_sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(StudentProfile, related_name='join_received_requests', on_delete=models.CASCADE) # Always leader
    temp_group = models.ForeignKey(TemporaryGroup, on_delete=models.CASCADE, related_name='join_requests')

    class Meta:
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f"{self.sender.username} → Leader {self.receiver.username} (join TempGroup {self.temp_group.id})"