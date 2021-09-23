from django.conf import settings

import asyncio
import aio_pika
from aio_pika.pool import Pool

"""
[No esta funcionando de forma async]

Returns:
    [type]: [AsyncMQ]
    
"""
class MQServiceAsync(object):
    
    def __init__(self):
        self.config = getattr(settings,'CONFIG_APP')
        self.loop = asyncio.get_event_loop()
        
    async def initial(self):
        self.connection_pool = Pool(self.get_connection, max_size=2, loop=self.loop)
        self.channel_pool = Pool(self.get_channel, max_size=10, loop=self.loop)
        self.queue_name = "user-messages"
        
                 
    async def get_connection(self):
        url = "amqp://{}:{}@{}:{}/{}".format(self.config["app"]["mservice"]['user'],
                                             self.config["app"]["mservice"]['passwd'],
                                             self.config["app"]["mservice"]['host'],
                                             self.config["app"]["mservice"]['port'],
                                             self.config["app"]["mservice"]['vhost'])
        await aio_pika.connect_robust(url)
        
    async def get_channel() -> aio_pika.Channel:
        async with self.connection_pool.acquire() as connection:
            return await connection.channel()
        
    async def consume(self):
        async with self.channel_pool.acquire() as channel:
            await channel.set_qos(1)
            queue = await channel.declare_queue(
                self.queue_name, durable=False, auto_delete=False)
            
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    print("Hay mensaje")
                    print(message)
                    #await message.ack()
        print("al final Hay mensaje")
            
    async def foreverRun(self):
        
        await self.initial()
        
        if (not self.loop.is_running()):
            task = self.loop.create_task(self.consume)
            await task
            print(" [*] Waiting for messages. To exit press CTRL+C")
            self.loop.run_forever()
        else:
            print("Event loop running")
    
    def run(self):
        resultado = asyncio.run(self.foreverRun())
        print(resultado)
        
        
            
        
        
        
        
    
    

