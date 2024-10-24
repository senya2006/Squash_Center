from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from accounts.models import Player


@admin.register(Player)
class PlayerAdmin(BaseUserAdmin):
    # Fields to be displayed in the list of users
    list_display = (
        'email',
        'first_name',
        'last_name',
        'phone_number',
        'is_active',
        'is_staff',
        'is_superuser',
        'avatar_tag',
    )

    # Fields to be searched
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')

    # Filters by field
    list_filter = ('is_active', 'is_staff', 'is_superuser')

    # Fields for editing
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Personal info'),
            {'fields': ('first_name', 'last_name', 'phone_number', 'birthday', 'photo', 'avatar_tag')},
        ),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )

    # Fields for creating a new user
    add_fieldsets = (
        (
            None,
            {
                'classes': ('wide',),
                'fields': (
                    'email',
                    'first_name',
                    'last_name',
                    'phone_number',
                    'password1',
                    'password2',
                    'is_active',
                    'is_staff',
                    'is_superuser',
                ),
            },
        ),
    )

    # Fields to be displayed in the create/edit form
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

    # Display avatar in the user list
    def avatar_tag(self, obj):
        if obj.photo:
            return format_html(f'<img src="{obj.photo.url}" style="width: 50px; height: 50px; border-radius: 50%;">')
        return "-"

    avatar_tag.short_description = 'Avatar'

    # Hide the avatar field as read-only so that it cannot be edited directly in the list
    readonly_fields = ['avatar_tag']
