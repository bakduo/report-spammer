
from django import forms

from tinymce.widgets import TinyMCE

class ReporterForm(forms.Form):
    
    email = forms.EmailField(required=True)
    domain = forms.CharField(max_length=50,required=True)
    description = forms.CharField(widget=TinyMCE(),required=True)
    ip = forms.GenericIPAddressField(required=True)
    emlfile = forms.FileField(required=False)


class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=TinyMCE(),required=True)
