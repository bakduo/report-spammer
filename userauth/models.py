from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.contrib import admin

# Create your models here.

from logging import getLogger

logger = getLogger(__name__)

# def validate_email(value):
#     if CustomUser.objects.filter(email = value).exists():
#         logger.info("Validador de email de usuario fomulario: {}".format(value))
#         raise ValidationError((f"{value} is taken."),params = {'value':value})
    
# def validate_username(value):
#     if CustomUser.objects.filter(username = value).exists():
#         logger.info("Validador de username de usuario fomulario: {}".format(value))
#         raise ValidationError((f"{value} is taken."),params = {'value':value})
    

#Modif gracias a https://github.com/astikgabani/Inventory-Management/blob/main/InventoryManagement/employees_api/models.py
# class UserType(models.Choices):
#     USER_APP = "User classic"
#     IT_ADMIN = "Super admin app"
#No hace falta porque se puede ejercer desde el admin setup


class RoleUser(models.Model):
    role = models.ForeignKey('Role',on_delete=models.CASCADE)
    user = models.ForeignKey('CustomUser',on_delete=models.CASCADE)

class Role(models.Model):
    name = models.CharField(verbose_name="Role user",
        max_length=255,unique=True, error_messages={
            'unique': ("This role already exists."),
        },)
    
    appname = models.CharField(verbose_name="Aplication for user",
        max_length=255,unique=True, error_messages={
            'unique': ("This application already exists."),
        },)
    
    date_start = models.DateField(default=timezone.now)

    date_end = models.DateField(default=timezone.now)

    is_on_user = models.ManyToManyField('CustomUser', through=RoleUser)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Role"
        verbose_name_plural = "Roles"
        ordering = ('date_start',)

#class CustomUser(AbstractBaseUser, PermissionsMixin):
class CustomUser(AbstractUser):
    
    email = models.EmailField(verbose_name="Email address",
        max_length=255,unique=True, error_messages={
            'unique': ("This email already exists."),
        },)
    
    username = models.CharField(verbose_name="Username",
        max_length=255,unique=True, error_messages={
            'unique': ("This username already exists."),
        },)
    
    created_at = models.DateTimeField(default=timezone.now)
    
    updated_at = models.DateTimeField(default=timezone.now)

    #type = models.CharField(max_length=120, choices=UserType.choices, default=UserType.USER_APP)
    
    role_by = models.ManyToManyField('Role', through=RoleUser)


    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ('email','username')


##Valido https://docs.djangoproject.com/en/4.2/ref/contrib/admin/
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    pass