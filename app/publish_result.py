import pika, os, sys
from json import dumps

def publish_result(result):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=os.getenv("RMQ_HOST")))  # connect to rmq
    channel = connection.channel()  # create a channel (we interact through channels)

    channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')  # create a rabbitmq EXCHANGE to publish to

    message = dumps(result)  # convert json back to string because we uased a json input
    channel.basic_publish(exchange='test_exchange', routing_key='', body=message)  # do the publish
    connection.close()
    return