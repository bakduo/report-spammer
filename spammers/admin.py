from django.contrib import admin

# Register your models here.

from .models import SpamMessage, SpamIp

def setTodo(modeladmin,request,queryset):
    queryset.update(state='todo')
    
def setProcessing(modeladmin,request,queryset):
    queryset.update(state='processing')

def setFinished(modeladmin,request,queryset):
    queryset.update(state='finished')
    
def setQueue(modeladmin,request,queryset):
    queryset.update(state='queue')
    
class SpamMessageAdmin(admin.ModelAdmin):
    list_display = ['email','domain','time','emlfile','type_of_state']
    ordering = ['time','email']
    list_filter = ('email','time','domain')
    actions = [setTodo,setFinished,setQueue,setProcessing]

admin.site.register(SpamIp)

admin.site.register(SpamMessage,SpamMessageAdmin)