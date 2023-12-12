import uuid
from contextlib import asynccontextmanager

import beanie
import structlog
from fastapi import FastAPI, Request, status
from fastapi.responses import ORJSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from .api import healthcheck
from .api.v1 import appraisal, bookmark, review
from .core.settings import settings
from .db import mongo
from .models import Bookmark, Review


@asynccontextmanager
async def lifespan(app: FastAPI):
    mongo_client = AsyncIOMotorClient(settings.mongo_url, uuidRepresentation="standard")  # type: ignore
    mongo.mongo_client = mongo_client
    await beanie.init_beanie(database=mongo_client.ugc, document_models=[Review, Bookmark])  # type: ignore
    yield
    mongo_client.close()


app = FastAPI(
    title="UGC service",
    description="Service for serving user content",
    version="0.0.1",
    docs_url="/api/openapi",
    openapi_url="/api/openapi.json",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)
logger = structlog.get_logger()


@app.middleware("http")
async def schema_correct(request: Request, call_next):
    scheme = "https" if request.headers.get("X-Forwarded-Proto") == "https" else "http"
    request.scope["scheme"] = scheme

    response = await call_next(request)

    return response


@app.middleware("http")
async def logger_middleware(request: Request, call_next):
    # Clear previous context variables
    structlog.contextvars.clear_contextvars()

    # Bind new variables identifying the request and a generated UUID
    request_id = request.headers.get("X-Request-Id") or str(uuid.uuid4())
    structlog.contextvars.bind_contextvars(
        path=request.url.path,
        method=request.method,
        client_host=request.client.host,  # type: ignore
        request_id=request_id,
    )

    # Make the request and receive a response
    response = await call_next(request)

    # Bind the status code of the response
    structlog.contextvars.bind_contextvars(
        status_code=response.status_code,
    )

    if status.HTTP_400_BAD_REQUEST <= response.status_code < status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.warn("Client error")
    elif response.status_code >= status.HTTP_500_INTERNAL_SERVER_ERROR:
        logger.error("Server error")
    else:
        logger.info("OK")

    return response


app.include_router(healthcheck.router)
app.include_router(review.router, prefix="/api/v1/review")
app.include_router(appraisal.router, prefix="/api/v1/appraisal")
app.include_router(bookmark.router, prefix="/api/v1/bookmark")
