from __future__ import absolute_import, unicode_literals

from celery import shared_task

from .mqservice import MQService

import logging

logger = logging.getLogger(__name__)

@shared_task(bind=True,name='consume_message')
def mqservice(self):
    try:
        logger.info("Initiate app..")
        mq = MQService.getInstance()
        mq.run()
    except Exception as e:
        logger.debug("Error app {}".format(e))