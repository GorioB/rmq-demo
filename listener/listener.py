import pika, os, sys, time

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RMQ_HOST')))
    channel = connection.channel()

    channel.exchange_declare(exchange='test_exchange', exchange_type='fanout')
    channel.queue_declare(queue='test_queue')
    channel.queue_bind(exchange='test_exchange', queue='test_queue')

    def callback(ch, method, properties, body):
        print(f"[+] Message Received: ${body}")

    channel.basic_consume(queue='test_queue', on_message_callback=callback, auto_ack=True)

    print("[+] Waiting for messages. Press CTRL+C to exit.")
    channel.start_consuming()

if __name__ == '__main__':
    try:
        retries = 3
        while retries:
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
