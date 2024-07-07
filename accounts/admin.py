from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "email",
                    "last_name",
                    "first_name",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
    search_fields = ("username", "email")
    list_display = ("username", "email", "first_name", "last_name", "is_staff")
