from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'auth_provider', 'created_at','client_ip','rating','feedback_text']

admin.site.register(User, UserAdmin)
