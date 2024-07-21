# from fastapi import FastAPI
#
# from services.auth import routes as AuthRoutes
# from services.books import routes as ProductRoutes
# from services.order import routes as OrderRoutes
# from services.rabbitmq_client import connect_rabbitmq_clients, \
#     get_inventory_rabbitmq_client, shutdown_rabbitmq_clients
#
# app = FastAPI()
#
# app.include_router(AuthRoutes.router)
# app.include_router(ProductRoutes.router)
# app.include_router(OrderRoutes.router)
#
#
# @app.on_event("startup")
# async def startup_event():
#     connect_rabbitmq_clients()
#     rabbitmq_client = get_inventory_rabbitmq_client()
#     rabbitmq_client.consume(callback=ProductRoutes.process_order)
#
#
# @app.on_event("shutdown")
# async def shutdown_event():
#     shutdown_rabbitmq_clients()
