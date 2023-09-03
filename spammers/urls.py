from django.urls import path
from .views import view_spammers, view_form, process_form, view_spammer_detail,view_file
from authdj import settings
from django.conf.urls.static import static


urlpatterns = [
    path("",view_spammers,name='email_list'),
    #path("eml/",view_file,name='spam_file'),
    path("reportspam/",view_form,name='email_form'),
    path("save/",process_form,name='spam_check'),
    path("detail/<slug:id>",view_spammer_detail,name='email_detail'),
]


#Para ver los archivos que se subieron en modo debug
if settings.DEBUG:
    urlpatterns += static(
        "eml/", document_root=str(settings.BASE_DIR.joinpath('eml'))
    )