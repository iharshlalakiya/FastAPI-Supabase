from fastapi import FastAPI
from src.api.routes import auth

app = FastAPI()

app.include_router(auth.router)