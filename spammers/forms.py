
from django import forms

from tinymce.widgets import TinyMCE
#from .models import SpamMessage

class ReporterForm(forms.Form):
    
    email = forms.EmailField(required=True)
    domain = forms.CharField(max_length=50,required=True)
    description = forms.CharField(widget=TinyMCE(attrs={'cols': 90, 'rows': 8}),required=True)
    ip = forms.GenericIPAddressField(required=True)
    emlfile = forms.FileField(required=False)
