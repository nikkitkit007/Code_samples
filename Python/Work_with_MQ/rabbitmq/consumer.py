from pydantic import BaseModel
import logging
import aiormq
import asyncio

RM_HOST: str = 'localhost'
RM_PORT: int = 5672
RM_USER: str = 'rmuser'
RM_PASSWORD: str = 'rmpassword'

queue_name = 'camera_to_server'
RABBITMQ_URL = f'amqp://{RM_USER}:{RM_PASSWORD}@{RM_HOST}:{RM_PORT}'
CHECK_RABBIT_PERIOD = 10

class Message(BaseModel):
    body: str


async def do_smth(message_body: str):
    if message_body:
        payload = Message.model_validate_json(message_body)
        logging.info(f'message received: {payload}')


async def consume_messages():
    connection = await aiormq.connect(url=RABBITMQ_URL)
    channel = await connection.channel()
    await channel.queue_declare(queue_name)
    while True:
        message = await channel.basic_get(queue_name)
        if message:
            message_body = message.body.decode()
            await do_smth(message_body)
        await asyncio.sleep(CHECK_RABBIT_PERIOD)


async def start_message_consumer():
    logging.info('Start rabbit message consumer')
    while True:
        await consume_messages()


if __name__ == '__main__':
    asyncio.create_task(start_message_consumer())
