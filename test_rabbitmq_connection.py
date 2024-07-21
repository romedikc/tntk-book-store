
import pika

try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    print('Connected to RabbitMQ!')
    connection.close()
except pika.exceptions.AMQPConnectionError as e:
    print(f'Failed to connect to RabbitMQ: {e}')

