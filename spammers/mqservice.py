from django.conf import settings

#import threading

from time import sleep

#from threading import Lock, Thread
import pika
import json
from .models import SpamMessage
from .models import SpamIp
#from datetime import date, datetime
from django.db import transaction
#import asyncio

# import the logging library
import logging
# Get an instance of a logger
logger = logging.getLogger(__name__)


class InvalidModel(RuntimeError):
   def __init__(self, arg):
      self.args = arg
       
class InvalidAttribute(RuntimeError): 
   def __init__(self, arg): 
      self.args = arg

"""[MQService]

Es una clase que permite recepcionar los envios async para hacer un update de registros de mails sobre una DB relacional

Returns:
    [type]: [description]
"""

class MQService(object):
    __instance = None
    
    def __init__(self):
        if MQService.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            super()
            self.channel = None
            self.connection = None
            self.parameters = None
            self.config = None
            self.credentials = None
            self.running = False
            self.initial();
            logger.info("Se contruyo MQService")
            MQService.__instance = self        
    
    @staticmethod
    def getInstance():
        """ Static access method. """
        if MQService.__instance == None:
            MQService()
        return MQService.__instance
        
    
    def setRunning(self,state):
        self.running = state
        
    def getRunning(self):
        return self.running
    
    def initial(self):
        
        self.config = getattr(settings,'CONFIG_APP')
        self.credentials = pika.PlainCredentials(self.config["app"]["mservice"]['user'], self.config["app"]["mservice"]['passwd'])
        if self.config["app"]["mservice"]['secure']==0:
            self.parameters = pika.ConnectionParameters(host=self.config["app"]["mservice"]['host'], port=self.config["app"]["mservice"]['port'], 
                                                        virtual_host=self.config["app"]["mservice"]['vhost'], credentials=self.credentials,
                                                        blocked_connection_timeout=300,
                                                        socket_timeout=30)
        else:
            self.parameters = pika.ConnectionParameters(host=self.config["app"]["mservice"]['host'], port=self.config["app"]["mservice"]['port'],
                                                        virtual_host=self.config["app"]["mservice"]['vhost'], credentials=self.credentials,                                                        blocked_connection_timeout=300,
                                                        socket_timeout=30,
                                                        ssl=True)
    
    @transaction.atomic
    def delMessage(self,message):
        logger.info("delete message")
        #Delete all record with email equal parameter
        emails = SpamMessage.objects.filter(email=message['data']['email']).delete()
        logger.debug(emails)
        if (emails is not None):
            logger.info("Email Record delete")
        else:
            logger.debug("Delete record behavior doesn't know")
            
    @transaction.atomic        
    def addMessage(self,message):
        try:
            logger.info("add message")
            tmp = SpamMessage.objects.create(message=message['data']['message'],
                domain=message['data']['domain'],
                email=message['data']['email'],
                description=message['data']['description'],
                time=message['data']['time'])
            tmpip = SpamIp(email_id=tmp.id,ip=message['data']['ip'])
            tmpip.save()
            logger.info("Save OK")
        except Exception as e:
            logger.error("Message invalid")
            raise InvalidModel(e)
    
    def callback(self, ch, method, properties, body):
        try:
            
            logger.info(method)
            logger.info(body)
            message = json.loads(body)
            if message['type']=='delete':
                self.delMessage(message)
            elif message['type']=='save':
                self.addMessage(message)
            elif message['type']=='update':
                self.addMessage(message)
            
            logger.info(method.delivery_tag)
            ch.basic_ack(delivery_tag = method.delivery_tag)
            return message
        except Exception as e:
            logger.error("Error callback: {}".format(e))
            raise InvalidAttribute(e)
        
    def stop(self):
        try:
            self.running = False
            return True
        except Exception as error:
            logger.debug(str(error))
    
    def consume(self):
        ERROR = None
        try:
            self.running = True
            logger.info("Iniciando consumo")
            self.channel.basic_consume(self.config['app']['services']['queue'],on_message_callback=self.callback,auto_ack=False)
            self.channel.start_consuming()
        except Exception as error:
            ERROR = "CONSUME"
            logger.error("Error channel basic consume: {}".format(str(error)))
            #notify_admin_by_email(message)
            
        if ERROR != None:
            sleep(3)
            self.running = False
            logger.error('Retry...consumming')
            self.consume()
        else:
            logger.info('Termino consumo')
            
    def run(self):
        
        try:
            logger.info("Running mqservice")
            self.connection = self.connect(self.parameters)
            if self.connection.is_open:
                if self.channel is None:
                    try:
                        self.channel = self.connection.channel()
                        self.channel.queue_declare(queue=self.config['app']['services']['queue'],durable=True,exclusive=False,auto_delete=False)
                        self.channel.queue_bind(queue=self.config['app']['services']['queue'],
                                                exchange=self.config['app']['services']['exchange'],routing_key="MSG")
                        self.channel.basic_qos(prefetch_count=1)
                        self.consume()
                    except Exception as error:
                        logger.error(str(error))
                        #notify_admin_by_email(message)
                        return error
                    
            else:
                logger.info("Conexion cerrada")
                #notify_admin_by_email(message)
                
        except Exception as error:
            logger.error('Error al generar INITIAL:', error.__class__.__class__)
             
    def connect(self,parameters):
        try:
            return pika.BlockingConnection(parameters)
        except Exception as error:
            logger.error('Error:', error.__class__.__name__)
