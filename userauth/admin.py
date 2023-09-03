from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from .models import Role, RoleUser

admin.site.register(Role)
admin.site.register(RoleUser)