from fastapi import FastAPI

from books import routes
from root.rabbitmq_client import get_inventory_rabbitmq_client

app = FastAPI()

app.include_router(routes.router)


@app.on_event("startup")
async def startup_event():
    try:

        rabbitmq_client = get_inventory_rabbitmq_client()
        rabbitmq_client.connect()
        # rabbitmq_client.consume(callback=routes.process_order)
    except Exception as e:
        print(f"Failed to connect or consume from RabbitMQ: {e}")


@app.on_event("shutdown")
async def shutdown_event():
    try:
        rabbitmq_client = get_inventory_rabbitmq_client()
        rabbitmq_client.disconnect()
    except Exception as e:
        print(f"Failed to disconnect from RabbitMQ: {e}")
