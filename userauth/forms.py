from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from .models import CustomUser
#from django.core.exceptions import ValidationError

#import log
from logging import getLogger

logger = getLogger(__name__)


from django.core.validators import validate_email

from django.core.validators import RegexValidator

validate_username = RegexValidator(regex=r'[a-zA-Z0-9]')

#No se puede validar en un formulario la existencia de un objeto persistido
#https://docs.djangoproject.com/en/1.10/ref/models/instances/#validating-objects
#def validate_email(value):
#     if CustomUser.objects.filter(email = value).exists():
#         logger.info("Validador de email de usuario fomulario: {}".format(value))
#         raise ValidationError((f"{value} is taken."),params = {'value':value})
    
#def validate_username(value):
#     if CustomUser.objects.filter(username = value).exists():
#         logger.info("Validador de username de usuario fomulario: {}".format(value))
#         raise ValidationError((f"{value} is taken."),params = {'value':value})

class RigisterUser(forms.Form):
    email = forms.EmailField(required=True,validators=[validate_email])
    username = forms.CharField(label="Username", validators=[validate_username],max_length=25,required=True)
    password=forms.CharField(widget=forms.PasswordInput(),required=True)
    confirm_password=forms.CharField(widget=forms.PasswordInput(),required=True)

    def clean(self):
        super().clean()
        password = self.cleaned_data.get("password")
        confirm_password = self.cleaned_data.get("confirm_password")
        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )


class CustomUserCreationForm(UserCreationForm):

    email = forms.EmailField(validators = [validate_email],required=True)
    username = forms.CharField(validators = [validate_username],label="Username", max_length=25,required=True)

    def clean(self):
       super().clean()
       password = self.cleaned_data.get("password")
       confirm_password = self.cleaned_data.get("confirm_password")
       if password != confirm_password:
           raise forms.ValidationError(
               "password no coincide, volver a intentar"
           )

class CustomUserChangeForm(UserChangeForm):

   class Meta:
       model = CustomUser
       fields = ['email','username']
