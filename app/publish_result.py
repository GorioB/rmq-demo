import pika, os, sys
from json import dumps

def publish_result(result):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv("RMQ_HOST")))
    channel = connection.channel()

    channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')

    message = dumps(result)  # convert json back to string because we uased a json input
    channel.basic_publish(exchange='test_exchange', routing_key='', body=message)
    connection.close()
    return