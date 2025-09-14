import http
import logging

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from api.helpers.logger_builder import LoggerBuilder
from api.config import settings
from api.controller import rag_router, status_router


logger = logging.getLogger(LoggerBuilder.name)

app = FastAPI(**settings.general_config)

app.include_router(rag_router)
app.include_router(status_router)

logger.info("Application started")


@app.exception_handler(Exception)
async def exception_handler(exc):
    logger.error(f"{exc}")
    return JSONResponse(
        status_code=http.HTTPStatus.INTERNAL_SERVER_ERROR, error=str(exc)
    )
