from django.contrib import admin
from .models import Group, GroupRequest

# Register your models here.

@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ('id', 'class_instance', 'is_finalized', 'member_count')
    list_filter = ('is_finalized', 'class_instance')
    search_fields = ('class_instance__name',)
    filter_horizontal = ('members',)
    readonly_fields = ('member_count',)

    def member_count(self, obj):
        return obj.members.count()
    member_count.short_description = 'Member Count'


@admin.register(GroupRequest)
class GroupRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'sender', 'receiver', 'group')
    search_fields = ('sender__user__username', 'receiver__user__username')
    list_filter = ('group',)