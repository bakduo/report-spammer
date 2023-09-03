from django.shortcuts import render
from django.shortcuts import redirect
from django.db import IntegrityError


from django.urls import reverse_lazy
from django.views import generic
from .forms import CustomUserCreationForm, RigisterUser
from django.db import transaction

##Modelos
from .models import CustomUser, Role, RoleUser

##Validadores

from django.core.validators import RegexValidator
from django.core.validators import validate_email
from django.core.exceptions import ValidationError,  ObjectDoesNotExist


validate_username = RegexValidator(regex=r'[a-zA-Z0-9]')

validate_password = RegexValidator(regex=r'^[\w+\d+|\d+\w+)+$]')

# Create your views here.
#from django.http import HttpResponse

#import message platform
from django.contrib import messages

#import log
from logging import getLogger

logger = getLogger(__name__)


def home_user_view(request):
    return redirect("/")

# class SignupPageView(generic.CreateView):
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'registration/signup.html'

def view_form(request):
    logger.info("Acceso a la vista de formulario")
    if request.method == 'GET':
        formUser= RigisterUser()
        return render(request, 'registration/form.html',{'form':formUser})
    
    return render(request, '404')


#proceso de alta de registro de usuario
@transaction.atomic
def process_form_user(request):
    ERROR_FORM = False
    logger.info("Acceso a sign up por medio de form")
    if request.method == 'POST':
        form = RigisterUser(request.POST)
        if (form.is_valid):
            
            logger.info("formulario enviado ok {}".format(request.POST))

            #Controlla exception de persistencia en todo los relacionado al modelo

            try:
                validate_email(form['email'].data)
            except ValidationError as e:
                logger.debug("El mail no es valido")
                ERROR_FORM = True
                messages.error(request,"El mail no es valido")
            try:
                validate_username(form['username'].data)
            except ValidationError as e:
                logger.debug("El username no es valido")
                ERROR_FORM = True
                messages.error(request,"El username no es valido")
            
            validate_password(form['password'].data)
            if form['password'].data != form['confirm_password'].data:
                ERROR_FORM = True
                messages.error(request,"La password no coincide")

            if not ERROR_FORM:

                try:
                    try:
                        role = Role.objects.get(name='USER',appname='Spam')
                        
                    except ObjectDoesNotExist:
                        role = Role(name='USER',appname='Spam')
                        role.save()
                        
                    try:
                        #user = CustomUser(username=form['username'].data,email=form['email'].data,password=form['password'].data)
                        user = CustomUser.objects.create(email=form['email'].data,username=form['username'].data,password=form['password'].data)
                        ##Sin este metodo la password queda en plano al margen que este utilizanso usermanager nuevo
                        user.set_password(form['password'].data)
                        user.save()
                        #user =  user.create_user_custom(email=form['email'].data,username=form['username'].data,password=form['password'].data)
                    except ValidationError as e:
                        ERROR_FORM = True
                        logger.debug("Problema con la validación del usuario: {}".format(e))
                        messages.error(request,"Problema con la validación del usuario: {}".format(e))    
                    except IntegrityError as e:
                        ERROR_FORM = True
                        logger.debug("Problema con la integridad del usuario: {}".format(e))
                        messages.error(request,"Problema con la integridad del usuario: {}".format(e))

                    try:
                        if not ERROR_FORM:
                            RoleUser(user=user, role=role).save()
                    except ValidationError as e:
                        ERROR_FORM = True
                        logger.debug("Problema con la validación de roles y usuario: {}".format(e))
                        messages.error(request,"Problema con la validación de roles y usuario: {}".format(e))
                    except IntegrityError as e:
                        ERROR_FORM = True
                        logger.debug("Problema con la integridad de roles y usuario: {}".format(e))
                        messages.error(request,"Problema con la integridad de roles y usuario: {}".format(e))

                    if not ERROR_FORM:
                       logger.debug("user id: {}".format(user.id))
                       logger.debug("role id: {}".format(role.id))
                       messages.success(request,"Se registro correctamente")
                       logger.info("datos {}".format(form['email'].data))

                except ValidationError as e:
                    logger.debug("Falla guardar los datos del formulario")
                    ERROR_FORM = True
                    messages.error(request,"Falla guardar los datos del formulario")
                
            #En caso de error retorno el formulario con el mensaje
            #Caso contrario retorno mensaje concluido

            return render(request, 'registration/form.html',{'form':form})
        
        else:
            formUser = RigisterUser()
            messages.error(request,"El formulario no es valido")
            return render(request, 'registration/form.html',{'form':formUser})
            
        
    return redirect("/")