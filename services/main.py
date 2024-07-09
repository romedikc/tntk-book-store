import atexit

from fastapi import FastAPI

from services import rabbitmq
from services.auth import routes as AuthRoutes
from services.books import routes as ProductRoutes
from services.order import routes as OrderRoutes

app = FastAPI()

app.include_router(AuthRoutes.router)
app.include_router(ProductRoutes.router)
app.include_router(OrderRoutes.router)

# RabbitMQ clients
order_rabbitmq_client = OrderRabbitMQClient(host='localhost', queue='order_queue')
order_rabbitmq_client.connect()

inventory_rabbitmq_client = InventoryRabbitMQClient(host='localhost', queue='order_queue')
inventory_rabbitmq_client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    order_rabbitmq_client.disconnect()
    inventory_rabbitmq_client.disconnect()


atexit.register(order_rabbitmq_client.disconnect)
atexit.register(inventory_rabbitmq_client.disconnect)


# Dependency to get RabbitMQ client instances
def get_order_rabbitmq_client():
    return order_rabbitmq_client


def get_inventory_rabbitmq_client():
    return inventory_rabbitmq_client


# Start consuming messages in the product service
@app.on_event("startup")
async def startup_event():
    inventory_rabbitmq_client.consume(callback=ProductRoutes.process_order)
