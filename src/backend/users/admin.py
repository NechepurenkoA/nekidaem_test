from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    """ "Админка пользователей."""

    list_display = (
        "username",
        "email",
    )
    search_fields = ("username",)
    list_filter = ("username",)
    empty_value_display = "-пусто-"
