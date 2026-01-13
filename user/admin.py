from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    list_display = (
        "id",
        "username",
        "email",
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
        "date_joined",
    )

    list_filter = (
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    ordering = ("-date_joined",)

    fieldsets = (
        ("Login Info", {
            "fields": ("username", "password")
        }),
        ("Personal Info", {
            "fields": ("first_name", "last_name", "email")
        }),
        ("Role & Permissions", {
            "fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Important Dates", {
            "fields": ("last_login", "date_joined")
        }),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("username", "email", "role", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )

    readonly_fields = ("date_joined", "last_login")