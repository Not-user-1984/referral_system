from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'invite_code', 'is_active')
    search_fields = ('phone_number', 'invite_code')

