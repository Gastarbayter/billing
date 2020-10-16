from fastapi import FastAPI
from markdown2 import markdown_path

from billing.api import views
from billing.app.config import settings
from billing.app.logging import init_logging
from billing.db.engine import db


def create_app():
    init_logging()

    app = FastAPI(title='billing', description=markdown_path(settings.README_PATH))
    # app.add_middleware(BaseHTTPMiddleware)

    app.include_router(views.routes, prefix='/v1', tags=['v1'])

    @app.on_event("startup")
    async def startup():
        await db.connect()

    @app.on_event("shutdown")
    async def shutdown():
        await db.disconnect()

    return app
