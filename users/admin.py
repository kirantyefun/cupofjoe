from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserChangeForm, CustomUserCreationForm
from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ("email", "username", "is_staff", "is_active", "is_cafe_owner", "has_cafe_registered")
    list_filter = ("email", "username", "is_staff", "is_active", "is_cafe_owner", "has_cafe_registered")
    fieldsets = (
        (None, {"fields": ("email", "username", "password", "is_cafe_owner", "has_cafe_registered")}),
        ("Permissions", {"fields": ("is_staff", "is_active", "groups", "user_permissions")})
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email", "username", "password1", "password2", "is_staff",
                "is_active", "groups", "user_permissions", "is_cafe_owner", "has_cafe_registerd",
            )
        }),
    )
    search_fields = ("email", "username")
    ordering = ("email", "username")


admin.site.register(CustomUser, CustomUserAdmin)