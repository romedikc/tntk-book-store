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
        if not self.channel:
            self.connect()
            if not self.channel:
                return
        try:
            self.channel.basic_publish(exchange='', routing_key=self.queue, body=json.dumps(message))
        except Exception as e:
            print(f"Failed to publish message: {e}")

    def consume(self, callback):
        if not self.channel:
            print("No channel found, attempting to reconnect")
            self.connect()
            if not self.channel:
                print("Failed to reconnect to RabbitMQ")
                return

        def on_message(ch, method, properties, body):
            try:
                message = json.loads(body)
                callback(message)
            except Exception as e:
                print(f"Failed to process message: {e}")

        try:
            self.channel.basic_consume(queue=self.queue, on_message_callback=on_message, auto_ack=True)
            print(f"Started consuming messages from queue {self.queue}")
            self.channel.start_consuming()
        except Exception as e:
            print(f"Failed to consume messages: {e}")
