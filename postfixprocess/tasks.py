import logging

logger = logging.getLogger(__name__)

from .sshservice import SSHService

from celery import shared_task

from messageadmin.settings import CONFIG_APP

@shared_task(bind=True,name='execute_remote_command')
def execute_remote_code(self):
    try:
        logger.info("Initiate app..")
        
        ssh = SSHService()
        
        comando = ""
        
        (stdoutstring, stderrstring) = ssh(CONFIG_APP['app']['services']['ip'], 
                                           CONFIG_APP['app']['services']['port'], 
                                           CONFIG_APP['app']['services']['user'], '',
                                           CONFIG_APP['app']['services']['keyfile'], None, comando)
        
        message = []
        
        if stderrstring is not None:
            for stdoutrow in stderrstring:
                message.append(stdoutrow)
            return message
            
        for stdoutrow in stdoutstring:
            message.append(stdoutrow)
             
        return message
    
    except Exception as e:
        logger.debug("Error app {}".format(e))