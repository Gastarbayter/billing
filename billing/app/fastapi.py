import logging

from fastapi import FastAPI
from markdown2 import markdown_path
from starlette.responses import JSONResponse

from billing.api import views
from billing.app.config import settings
from billing.app.logging import init_logging
from billing.db.engine import db
from billing.errors import exception


def create_app():
    init_logging()

    fast_app = FastAPI(title='billing', description=markdown_path(settings.README_PATH))

    fast_app.include_router(views.routes, prefix='/v1', tags=['v1'])

    return fast_app


app = create_app()


@app.on_event('startup')
async def startup():
    await db.connect()


@app.on_event('shutdown')
async def shutdown():
    await db.disconnect()


logger = logging.getLogger(settings.APP_NAME)


@app.exception_handler(exception.BaseError)
async def http_exception_handler(_, ex: exception.BaseError):
    logger.error(ex)
    return JSONResponse(
        status_code=ex.status_code,
        content={
            'detail': ex.detail,
            'message': ex.message,
        },
    )
