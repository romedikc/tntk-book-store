from fastapi import FastAPI

from order import routes
from root.rabbitmq_client import get_order_rabbitmq_client
from root.redis import redis_client

app = FastAPI()

app.include_router(routes.router)


@app.on_event("startup")
async def startup_event():
    rabbitmq_client = get_order_rabbitmq_client()
    rabbitmq_client.connect()
    redis_client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    rabbitmq_client = get_order_rabbitmq_client()
    rabbitmq_client.disconnect()
