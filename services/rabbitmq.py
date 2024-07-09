import pika
import json


class RabbitMQClient:
    def __init__(self, host: str, queue: str):
        self.host = host
        self.queue = queue
        self.connection = None
        self.channel = None

    def connect(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue)

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def publish(self, message: dict):
        self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(message))

    def consume(self, callback):
        def on_message(ch, method, properties, body):
            message = json.loads(body)
            callback(message)

        self.channel.basic_consume(queue=self.queue, on_message_callback=on_message, auto_ack=True)
        self.channel.start_consuming()
