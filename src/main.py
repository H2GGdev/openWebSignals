import logging
from fastapi import FastAPI, Request
from src.routes import analyze, health
import time

# --------------------------
# Setup basic logging
# --------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

app = FastAPI(title="Website Intelligence API")
app.include_router(analyze.router)
app.include_router(health.router)

# --------------------------
# Middleware to log requests with response time
# --------------------------
@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time_ms = (time.time() - start_time) * 1000
    logging.info(
        f"{request.method} {request.url.path} completed in {process_time_ms:.2f}ms "
        f"status_code={response.status_code}"
    )
    return response



"""from fastapi import FastAPI
from src.routes import analyze, health

app = FastAPI(title="Website Intelligence API")
app.include_router(analyze.router)
app.include_router(health.router)
"""