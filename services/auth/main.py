from fastapi import FastAPI

from services.auth import routes

app = FastAPI()

app.include_router(routes.router)
