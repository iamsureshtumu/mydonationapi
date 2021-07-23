from django.contrib import admin

# Register your models here.
from .models import *


class UserAdmin(admin.ModelAdmin):
    list_display = [ 'id', 'first_name', 'last_name', 'email', 'no_of_transactions', 'auth_provider', 'created_at', 'updated_at', 'client_ip' ] #'rating', 'feedback_text'

class Anonymous(admin.ModelAdmin):
        list_display = ['rating', 'feedback_text']


class Guest(admin.ModelAdmin):
    list_display = ['secret_key', 'transaction_successful_ID', 'first_name', 'last_name', 'email', 'portfolio_name', 'amount', 'charities', 'created_at', 'updated_at', 'client_ip' ]

class UserTXn(admin.ModelAdmin):
    list_display = ['user_id', 'referrence_number', 'transaction_successful_ID', 'portfolio_name', 'amount', 'charities',]


admin.site.register(User, UserAdmin)
admin.site.register(RatingFeedback, Anonymous)
admin.site.register(GuestUser, Guest)
admin.site.register(UserTransaction,UserTXn)
