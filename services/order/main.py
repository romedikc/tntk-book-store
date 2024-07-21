from fastapi import FastAPI

from services.order import routes
from services.rabbitmq_client import get_order_rabbitmq_client

app = FastAPI()

app.include_router(routes.router)


@app.on_event("startup")
async def startup_event():
    rabbitmq_client = get_order_rabbitmq_client()
    rabbitmq_client.connect()


@app.on_event("shutdown")
async def shutdown_event():
    rabbitmq_client = get_order_rabbitmq_client()
    rabbitmq_client.disconnect()
