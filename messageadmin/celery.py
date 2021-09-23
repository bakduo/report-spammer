from __future__ import absolute_import, unicode_literals
from celery import Celery
import os
from .settings import CONFIG_APP

config = CONFIG_APP

url = "amqp://" + config["app"]["mcelery"]['user'] + ":" + config["app"]["mcelery"]['passwd'] + "@" + config["app"]["mcelery"]['host'] + ":" +  str(config["app"]["mservice"]['port']) + "/" + config["app"]["mcelery"]['vhost'];

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'messageadmin.settings');
    
app = Celery('messageadmin',
             broker=url,
             backend='rpc://')


app.config_from_object('django.conf:settings',namespace='CELERY')

app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

app.conf.beat_schedule = {
    'run_remote_command' : {
        'task':'execute_remote_command',
        'schedule': 4.0,
    }
}
if __name__ == '__main__':
    app.start()
