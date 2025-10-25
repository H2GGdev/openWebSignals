import logging
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from src.routes import analyze, health, documentation
import time

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = FastAPI(title="Website Intelligence API")
# Mount static assets at the app level so every route can reference /static/*
app.mount("/static", StaticFiles(directory="src/static"), name="static")

app.include_router(analyze.router)
app.include_router(health.router)
app.include_router(documentation.router)