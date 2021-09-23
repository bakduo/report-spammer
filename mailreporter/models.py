from django.utils import timezone
from django.db import models
from tinymce.models import HTMLField

# Create your models here.

"""[Modelo para para los mails de contactos, luego puede existir un batch de proceso que pueda enviar todos los correos de forma async y al mismo tiempo
realizar un check a fin de evitar enviar spam]

    Returns:
        [type]: [description]
"""
class ContactPerson(models.Model):
    email = models.EmailField(max_length = 100,blank=False,null=False)
    subject=models.CharField(max_length=100,blank=False,null=False)
    message=HTMLField(blank=False,null=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.email