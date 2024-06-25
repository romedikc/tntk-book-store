from fastapi import FastAPI

from services.auth import routes as AuthRoutes
from services.books import routes as TaskRoutes

app = FastAPI()

app.include_router(AuthRoutes.router)
app.include_router(TaskRoutes.router)
