from fastapi import APIRouter

from billing.api import (
    controllers,
    serializers,
)


routes = APIRouter()


@routes.post(
    path='/clients',
    response_description='Создание клиента',
    summary='Создание клиента с кошельком',
    status_code=201,
    response_model=serializers.ClientResponse,
)
async def create_client(client: serializers.ClientRequests):
    client: dict = await controllers.create_client_with_wallet(client=client)
    return client


@routes.post(
    path='/transfer',
    response_description='Перевод денежных средств с одного кошелька на другой',
    summary='Денежный перевод',
    status_code=201,
    response_model=serializers.TransferResponse,
)
async def create_transfer(transfer: serializers.TransferRequests):
    transfer: dict = await controllers.create_transfer(transfer=transfer)
    return transfer


@routes.post(
    path='/replenishment',
    response_description='Зачисление денежных средств на кошелек клиента',
    summary='Пополнение счета клиента',
    status_code=201,
    response_model=serializers.ReplenishmentResponse,
)
async def create_replenishment(replenishment: serializers.ReplenishmentRequests):
    replenishment: dict = await controllers.create_replenishment(replenishment=replenishment)
    return replenishment
