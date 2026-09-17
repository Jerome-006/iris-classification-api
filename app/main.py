from app.logging_config import setup_logging
from app.config import settings
import logging
import time
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import uuid

from app.routers.v1 import router as v1_router
from app.routers.v2 import router as v2_router
from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(title=settings.API_TITLE)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["X-API-Key", "Content-Type"],
)


app.include_router(v1_router)
app.include_router(v2_router)


Instrumentator().instrument(app).expose(app)


setup_logging()
logger = logging.getLogger(__name__)


@app.middleware("http")
async def logging_middleware(request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    start_time = time.time()

    response = await call_next(request)

    duration = time.time() - start_time

    logger.info(
        f"request_id={request_id} "
        f"method={request.method} "
        f"path={request.url.path} "
        f"duration={duration:.4f}s"
    )

    return response


@app.get("/")
def home():
    return {"message": "Iris API running"}