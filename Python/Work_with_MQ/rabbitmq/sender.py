#!/usr/bin/env python
import pika

credentials = pika.PlainCredentials('rmuser', 'rmpassword')

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', credentials=credentials))
channel = connection.channel()


def dif_queue():
    channel.queue_declare(queue='hello_1')

    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')

    channel.queue_declare(queue='hello_2')

    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')


def one_queue():
    channel.queue_declare(queue='hello_1')
    channel.basic_publish(exchange='', routing_key='hello', body='Hello World!')


for i in range(5):
    # dif_queue()
    one_queue()

print(" [x] Sent 'Hello World!'")
connection.close()
