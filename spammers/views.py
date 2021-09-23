from django.shortcuts import redirect
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.views import generic
from django.core.paginator import Paginator

from logging import getLogger
from django.http import JsonResponse

logger = getLogger(__name__)

# Create your views here.

from .tasks import mqservice
from .models import SpamMessage
from .mqservice import MQService
from .models import SpamIp

## Para realizar busquedas
from django.db.models import Q

def running(request):
    
    contenido = {}    

    if request.method == 'GET':
        try:
            #se puede ver tmb REMOTE_HOST
            if (request.META['REMOTE_ADDR']=="192.168.2.11"):
                if MQService.getInstance().running == False:
                    mqservice.delay()
                    contenido={'SUCCESS':'MQ Running',"fail":None}
            else:
                contenido={'SUCCESS':None,"fail":"No esta autorizado a iniciar desde otra ip"}
        except Exception as e:
            logger.debug("Ocurrio un error al iniciar servicio")
            contenido={'SUCCESS':None,"fail":"MQ don't run"}
    
        
    return JsonResponse(contenido, status=200)

class SpamMessageListView(generic.ListView):
    logger.info("Acceso a la vista de emails por medio de paginacion")
    model = SpamMessage
    paginate_by = 10
    
def view_spammers(request):
    logger.info("Acceso a la vista de emails")
    
    if (request.method=="GET"):
        search_email = request.GET.get('search')
        if (search_email is not None):
            emails = SpamMessage.objects.filter(Q(email__icontains=search_email))
        else:
            emails = SpamMessage.objects.all().order_by("-created_at")
    
    paginator = Paginator(emails, 25)
    
    if (request.method=="GET"):
        page_number = request.GET.get('page')
        if page_number is not None:
            page_obj = paginator.get_page(page_number)
        else:
            page_obj = paginator.get_page(0)
            
    return render(request, 'spammers/list.html', {'emails': page_obj})

def spammers_detail_view(request,**kwargs):
    
    logger.info("Acceso a la vista de detail")
    
    if (request.method == "GET"):
        ##Aqui se puede mejorar un poco más
        spam = get_object_or_404(SpamMessage, id=kwargs.get('id'))
        dataIp = get_object_or_404(SpamIp,email_id=spam.id)
        compuesto = {
            'email':spam.email,
            'time':spam.time,
            'domain':spam.domain,
            'ip':dataIp.ip,
            'created_at':spam.created_at,
            'state':spam.state,
            'message':spam.message
        }
        return render(request,'spammers/detail.html',context={'email':compuesto})
    
    return redirect("/")
    