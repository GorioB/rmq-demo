import pika, os, sys, time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RMQ_HOST')))
    channel = connection.channel()  # connect to RMQ server and create a channel

    channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')  # create an exchange in case it doesn't exist yet
    channel.queue_declare(queue='test_queue')  # create the queue that receives messages from the exchange
    channel.queue_bind(exchange='test_exchange', queue='test_queue')  # tell the queue to listen to exchange

    def callback(ch, method, properties, body):  # the actual thing we do. in this case, just print the data
        print(f"[+] Message Received: ${body}")

    channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)  # listen to the queue and do callback if we get a message

    print("[+] Waiting for messages. Press CTRL+C to exit.")
    channel.start_consuming()

if __name__ == '__main__':
    try:
        retries = 3
        while retries:  # implemented a retry mechanism so that the server will wait until rmq is ready to accept connections
            try:
                main()
            except pika.exceptions.AMQPConnectionError:
                print("[-] Error connecting to rmq. Waiting 5s before trying again")
                time.sleep(5)
                retries -= 1
        print("[-] Exceeded retries, quitting.")
    except KeyboardInterrupt:
        print('Quitting')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
