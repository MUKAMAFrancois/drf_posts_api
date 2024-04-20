from django.contrib import admin
from .models import User

# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'date_joined', 'is_active', 'is_staff']
    search_fields = ['email', 'username']
    list_filter = ['is_active', 'is_staff']
    ordering = ['date_joined']

admin.site.register(User, UserAdmin)