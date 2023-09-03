from django.urls import path
from .views import view_spammers, view_form, process_form, view_spammer_detail
from authdj import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",view_spammers,name='email_list'),
    path("reportspam/",view_form,name='email_form'),
    path("save/",process_form,name='spam_check'),
    path("detail/<slug:id>",view_spammer_detail,name='email_detail'),

] + static("eml/",  document_root=str(settings.UPLOAD_FOLDER)+'/eml', show_indexes=False)