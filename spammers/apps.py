#from spammers.mqservice import MQService
from django.apps import AppConfig
import os

#from .tasks import delayed_task
#import asyncio

class SpammersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'spammers'
            
    def ready(self):
        pass
    #     #loop = asyncio.get_event_loop()
    #     #loop.run_in_executor(None,mq.run(),None)
    #     #task = [mq.run()]
    #     #loop.run_in_executor(None,mq.run())
    #     #loop.close()
    #     pass
    #     #loop.run_until_complete(self.mqservice())
        
        
