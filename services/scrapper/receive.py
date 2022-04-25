import pika, sys, os
from add_product import add_product
import json


def main():
    credentials = pika.PlainCredentials('root', 'root')
    props = {'connection_name': 'link scraping'}
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost',
                                                                   credentials=credentials,
                                                                   client_properties=props))
    channel = connection.channel()

    channel.queue_declare(queue='scrapped_links')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % json.loads(body))
        add_product([str(val) for val in json.loads(body).values()][0])
    channel.basic_consume(queue='scrapped_links', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
