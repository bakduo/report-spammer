from django.urls import path

from .views import view_form, process_form_user,home_user_view

urlpatterns  = [
    path('',home_user_view, name='home'),
    #path('signup/',SignupPageView.as_view(),name='signup'),
    path("signup/",view_form,name='sign_form'),
    path("save/",process_form_user,name='register_check'),
]