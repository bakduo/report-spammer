from django.urls import path

from .views import APIListSpamMessage, APIDetailSpamMessage

urlpatterns = [
    path("<int:pk>/",APIDetailSpamMessage.as_view(),name="spammessage_detail"),
    path("",APIListSpamMessage.as_view(),name="spammessage_list"),
]