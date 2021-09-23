from django.urls import path

from .views import view_spammers
from .views import spammers_detail_view
from .views import running

urlpatterns = [
    path("",view_spammers,name='email_list'),
    path("detail/<slug:id>",spammers_detail_view,name='email_detail'),
    path("run",running,name='mqrun')
]
