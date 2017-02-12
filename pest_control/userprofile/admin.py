from django.contrib import admin

from userprofile.models import UserProfile, Employee

admin.site.register(UserProfile)
admin.site.register(Employee)