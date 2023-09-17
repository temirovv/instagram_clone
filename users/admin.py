from django.contrib import admin
from .models import User, UserConfirmation


class UserModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'phone_number']

class UserConfimationModelAdmin(admin.ModelAdmin):
    list_display = ['code', 'verify_type', 'user', 'expiration_time', 'is_confirmed']

admin.site.register(User, UserModelAdmin)
admin.site.register(UserConfirmation, UserConfimationModelAdmin)
