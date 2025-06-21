from django.contrib import admin
from .models import Group, GroupRequest, TemporaryGroup

# Register your models here.

class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_instance', 'get_members', 'is_finalized')
    list_filter = ('is_finalized', 'class_instance')
    search_fields = ('class_instance__code', 'members__username')
    filter_horizontal = ('members',)

    def get_members(self, obj):
        return ", ".join([member.username for member in obj.members.all()])
    get_members.short_description = 'Members'


class GroupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'group')
    search_fields = ('sender__username', 'receiver__username')
    list_filter = ('group',)

class TemporaryGroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_instance', 'get_members', 'leader')
    search_fields = ('class_instance__code', 'members__username', 'leader__username')
    list_filter = ('class_instance',)
    filter_horizontal = ('members',)

    def get_members(self, obj):
        return ", ".join([m.username for m in obj.members.all()])
    get_members.short_description = 'Members'

admin.site.register(Group, GroupAdmin)
admin.site.register(GroupRequest, GroupRequestAdmin)
admin.site.register(TemporaryGroup, TemporaryGroupAdmin)