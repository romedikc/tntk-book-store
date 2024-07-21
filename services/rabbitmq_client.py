from services.rabbitmq import RabbitMQClient


def get_order_rabbitmq_client():
    return RabbitMQClient(host='rabbitmq', queue='order_queue')


def get_inventory_rabbitmq_client():
    return RabbitMQClient(host='rabbitmq', queue='books_queue')
