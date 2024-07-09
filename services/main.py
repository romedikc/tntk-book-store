from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from services.auth import routes as AuthRoutes
from services.books import routes as TaskRoutes
from services.order import routes as OrderRoutes

app = FastAPI()

app.include_router(AuthRoutes.router)
app.include_router(TaskRoutes.router)
app.include_router(OrderRoutes.router)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
