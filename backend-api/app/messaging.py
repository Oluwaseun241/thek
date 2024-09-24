import pika
import json

RABBITMQ_URL = "amqp://guest:guest@localhost/"

def send_message(action: str, book_id: str):
    connection = pika.BlockingConnection(pika.URLParameters(RABBITMQ_URL))
    channel = connection.channel()

    channel.queue_declare(queue='book_updates')

    message = f"{action}: {book_id}"
    channel.basic_publish(exchange='', routing_key='book_updates', body=json.dumps(message))
    print(f"Sent message: {message}")

    connection.close()
