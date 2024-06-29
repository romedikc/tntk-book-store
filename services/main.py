from fastapi import FastAPI

from services.auth import routes as AuthRoutes
from services.books import routes as TaskRoutes
from services.order import routes as OrderRoutes

app = FastAPI()

app.include_router(AuthRoutes.router)
app.include_router(TaskRoutes.router)
app.include_router(OrderRoutes.router)
