from django.db import transaction
from django.shortcuts import redirect, render

# Create your views here.

from django.shortcuts import render

from django.core.exceptions import ValidationError

from django.core.validators import validate_email

from django.core.validators import validate_ipv46_address, RegexValidator

validate_hostname = RegexValidator(regex=r'[a-zA-Z0-9-_]*\.[a-zA-Z]{2,6}')

from spammers.models import SpamMessage

from spammers.models import SpamIp

from .models import ContactPerson

from .forms import ReporterForm
from .forms import ContactForm

from logging import getLogger

from django.contrib import messages

import time


logger = getLogger(__name__)

def view_form(request):
    logger.info("Acceso a la vista de formulario")
    if request.method == 'GET':
        formSpam = ReporterForm()
        return render(request, 'mailreporter/form.html',{'form':formSpam})
    
    return render(request, '404')

@transaction.atomic
def contact_view(request):
    ERROR_FORM = False
    if request.method == 'GET':
        form = ContactForm()
        return render(request, "mailreporter/contact.html", {'form': form})
    else:
        form = ContactForm(request.POST)
        
        if form.is_valid():
        
            if form['subject'].data is None:
                ERROR_FORM = True
                messages.error(request,"Al menos indicar un subject")
                
            if form['message'].data is None:
                ERROR_FORM = True
                messages.error(request,"Al menos debe indicar un mensaje")
            
            try:
                validate_email(form['email'].data)
            except ValidationError as e:
                ERROR_FORM = True
                logger.debug("El mail no es valido")
                messages.error(request,"El mail no es valido")     
            
            if ERROR_FORM == False:
                try:
                    contacto = ContactPerson(email=form['email'].data,message=form['message'].data,subject=form['subject'].data)
                    contacto.save()
                    messages.success(request,"El mensaje fue procesado.")
                except Exception as e:
                    logger.debug("Error al procesar datos de contacto")
                    messages.error(request,"Error al procesar datos de contacto")
                    
                
            return render(request, 'mailreporter/contact.html',{'form':form})
        else:
            logger.debug("Formulario invalido")
            messages.error(request,"Formulario invalido")     
            return render(request, "mailreporter/contact.html", {'form': form})
            
            
        
    

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
                
                fecha = time.strftime("%y-%m-%d")
                if UPLOAD_FILE:
                    email_spam = SpamMessage(email=form['email'].data,domain=form['domain'].data,description=form['description'].data,
                                         emlfile=request.FILES['emlfile'],time=fecha,message="")
                else:
                    email_spam = SpamMessage(email=form['email'].data,domain=form['domain'].data,description=form['description'].data
                                             ,time=fecha,message="")
                
                email_spam.save()
                logger.debug("email id: {}".format(email_spam.id))
                ip_spam = SpamIp(email_id=email_spam.id,ip=(form['ip'].data))
                ip_spam.save()
                logger.debug("email id: {}".format(ip_spam.id))   
                messages.success(request,"Se registro correctamente")
                
            logger.info("datos {}".format(form['email'].data))
            return render(request, 'mailreporter/form.html',{'form':form})
        
        else:
            formSpam = ReporterForm()
            messages.error(request,"El formulario no es valido")
            return render(request, 'mailreporter/form.html',{'form':formSpam})
            
        
    return redirect("/")