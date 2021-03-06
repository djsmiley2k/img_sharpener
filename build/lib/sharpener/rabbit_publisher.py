import pika
import logging
from pika.credentials import PlainCredentials

__author__ = 'viaa'


def send_message(host, port, username, password, exchange, routing_key, queue, topic_type, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=host,
        port=int(port),
        credentials=PlainCredentials(username, password)
    ))
    channel = connection.channel()
    if queue is not None and topic_type is not None:
        channel.exchange_declare(exchange=exchange, type=topic_type)
        channel.queue_declare(queue=queue, durable=True)
        channel.queue_bind(queue=queue, exchange=exchange, routing_key=routing_key)
    channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
    connection.close()
    logging.info("Message published to: " + exchange + "/" + routing_key)
