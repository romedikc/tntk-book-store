from fastapi import FastAPI

from src.auth import routes as AuthRoutes
from src.tasks import routes as TaskRoutes

app = FastAPI()

app.include_router(AuthRoutes.router)
app.include_router(TaskRoutes.router)
