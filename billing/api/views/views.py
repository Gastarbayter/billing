from fastapi import APIRouter
from starlette.responses import JSONResponse

from billing.api import (
    controllers,
    serializers,
)


routes = APIRouter()


@routes.get(
    path='/clients/{client_id}',
    response_description="Клиент",
    summary='Получение клиента по идентифатору',
)
async def get_client(client_id: int):
    client = await controllers.get_client_by_id(client_id)
    return client


@routes.post(
    path='/clients',
    response_description="Создание клиента",
    summary='Создание клиента с кошельком',
    response_model=serializers.ClientRequests,
)
async def create_client(client: serializers.ClientRequests):
    raise NotImplementedError()
    # await controllers.create_client(client)
    # return JSONResponse(status_code=201)
