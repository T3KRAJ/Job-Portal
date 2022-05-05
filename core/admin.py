"""_summary_
Admin dashboard
@Author: Tek Raj Joshi
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Application, Category, Interview, Job, Message, RecruiterProfile, SeekerProfile, Subcategory, User, SeekerSkillset

# Custom user admin class inherting BaseUserAdmin
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('email', 'password', 'name', 'last_login')}),
        ('Permissions', {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
    )
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': ('email', 'password1', 'password2')
            }
        ),
    )

    list_display = ('email', 'name', 'is_staff', 'last_login')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

# Every models needs to be registered.
admin.site.register(SeekerProfile)
admin.site.register(RecruiterProfile)
admin.site.register(Job)
admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Message)
admin.site.register(Application)
admin.site.register(Interview)
admin.site.register(SeekerSkillset)
