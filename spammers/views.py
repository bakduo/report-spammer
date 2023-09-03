from django.shortcuts import render

from django.shortcuts import redirect

from django.db import transaction

from django.views import generic

from django.core.paginator import Paginator

from django.shortcuts import get_object_or_404

from logging import getLogger

#Validadores
from django.core.exceptions import ValidationError

from django.core.validators import validate_email

from django.core.validators import validate_ipv46_address, RegexValidator

from django.http import Http404

from django.utils.translation import gettext as _

##para trabajar con la fecha del reporte
import time

#import message platform
from django.contrib import messages

validate_hostname = RegexValidator(regex=r'[a-zA-Z0-9-_]*\.[a-zA-Z]{2,6}')
                                    
logger = getLogger(__name__)

ALLOWED_MIMETYPES = ("text/plain","application/pdf")

from .models import SpamMessage, SpamIp

from .forms import ReporterForm

#Control de mime type
#https://pypi.org/project/python-magic/
import magic

# Create your views here.

## Para realizar busquedas
from django.db.models import Q

from authdj.settings import BASE_DIR


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



def view_form(request):
    logger.info("Acceso a la vista de formulario")
    if request.method == 'GET':
        formSpam = ReporterForm()
        return render(request, 'spammers/form.html',{'form':formSpam})
    
    return render(request, '404')


def view_spammer_detail(request,**kwargs):
    
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


@transaction.atomic
def process_form(request):
    ERROR_FORM = False
    UPLOAD_FILE = True
    logger.info("Acceso a reporte de mail por medio de form")
    if request.method == 'POST':
        form = ReporterForm(request.POST, request.FILES)
        if (form.is_valid):
            logger.info("formulario enviado ok {}".format(request.POST))
            try:
                validate_email(form['email'].data)
            except ValidationError as e:
                logger.debug("El mail no es valido")
                ERROR_FORM = True
                messages.error(request,"El mail no es valido")
            try:
                validate_hostname(form['domain'].data)
            except ValidationError as e:
                logger.debug("El domain no es valido")
                ERROR_FORM = True
                messages.error(request,"El domain no es valido")
            
            try:
                validate_ipv46_address(form['ip'].data)
            except ValidationError as e:
                logger.debug("La ip no es valida")
                ERROR_FORM = True
                messages.error(request,"La ip no es valida")
                
            if form['emlfile'].data is None:
                UPLOAD_FILE = False
            
            if not ERROR_FORM:
                
                fecha = time.strftime("%Y-%m-%d")

                if UPLOAD_FILE:
                    mime_type = magic.from_buffer(request.FILES['emlfile'].read(), mime=True)
                    if mime_type in ALLOWED_MIMETYPES:
                        email_spam = SpamMessage(email=form['email'].data,domain=form['domain'].data,description=form['description'].data,
                                                 emlfile=request.FILES['emlfile'],time=fecha,message="")
                    else:
                        logger.debug("Contenido no valido para subir")
                        ERROR_FORM = True
                        messages.error(request,"El achivo no es valido para subir")
                else:
                    email_spam = SpamMessage(email=form['email'].data,domain=form['domain'].data,description=form['description'].data
                                             ,time=fecha,message="")
                if not ERROR_FORM:
                    email_spam.save()
                    logger.debug("email id: {}".format(email_spam.id))
                    ip_spam = SpamIp(email_id=email_spam.id,ip=(form['ip'].data))
                    ip_spam.save()
                    logger.debug("email id: {}".format(ip_spam.id))
                    messages.success(request,"Se registro correctamente")
                
            #logger.info("datos {}".format(form['email'].data))
            return render(request, 'spammers/form.html',{'form':form})
        
        else:
            formSpam = ReporterForm()
            messages.error(request,"El formulario no es valido")
            return render(request, 'spammers/form.html',{'form':formSpam})
            
        
    return redirect("/")


def download_file(path):
    logger.info("nada User autenticado")
    logger.info(path)
    raise Http404(_("Testing control no funciona."))