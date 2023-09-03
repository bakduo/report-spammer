from django.db import models

# Create your models here.
from django.utils import timezone

#from django.utils.html import format_html

from tinymce import models as tinymce_models


from django.urls import reverse

class SpamMessage(models.Model):
    STATE_MESSAGE = (('finished','finished'),('queue','queue'),('processing','processing'),('todo','todo'))
    message=models.CharField(max_length=255,blank=True,null=True)
    #description=models.TextField(blank=True,null=True)
    description=tinymce_models.HTMLField(blank=True,null=True)
    #time=models.CharField(max_length=35,null=True,blank=True)
    ##datetime.date(1962, 8, 16)
    time = models.DateField(null=True,blank=True)
    email=models.CharField(max_length=255,default='example@example.com',blank=False,null=False)
    domain=models.CharField(max_length=255,default='example.com',blank=False,null=False)
    emlfile=models.FileField(upload_to='./eml/%Y/%m/%d/',default='',blank=True,null=True)
    state=models.CharField(max_length=16,choices=STATE_MESSAGE,default='todo')
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def get_absolute_url(self):
        return reverse('email_detail', args=[str(self.id)])
    
    def type_of_state(self):
        return self.state
        """ 
        if self.state == 'todo':
            return format_html('<span stype="color:#ff0">{}</span>',self.state)
        elif self.state == 'queue':
            return format_html('<span stype="color:#f0f">{}</span>',self.state)
        elif self.state == 'processing':
            return format_html('<span stype="color:#099">{}</span>',self.state)
        elif self.state == 'finished':
            return format_html('<span stype="color:#019">{}</span>',self.state)
        """
        
    def __str__(self):
        return self.email
    
    class Meta:
        verbose_name = "SpamMessage"
        verbose_name_plural = "SpamMessages"
        ordering = ('created_at',)
    
    
class SpamIp(models.Model):
    email = models.ForeignKey('SpamMessage',verbose_name='SpamEmail', on_delete=models.CASCADE)
    ip = models.CharField(max_length=255,default='0.0.0.0',blank=False,null=False)
    description=models.CharField(max_length=255,blank=True,null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return self.ip
    
    class Meta:
        verbose_name = "SpamIp"
        verbose_name_plural = "SpamIps"
        ordering = ('created_at',)