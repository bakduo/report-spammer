from django.urls import path

from .views import view_form
from .views import process_form
from .views import contact_view

urlpatterns = [
    path("",view_form,name='email_form'),
    path("spam/",process_form,name='email_check'),
    path("contact/",contact_view,name='email_contact'),
]