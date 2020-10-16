from asyncpg import UniqueViolationError

from billing.api import serializers
from billing.api.controllers import wallet
from billing.db import models
from billing.db.engine import (
    db,
)
from billing.errors.exception import DuplicateClientExceptions


@db.transaction()
async def create_client_with_wallet(client: serializers.ClientRequests) -> dict:
    client_id: int = await create_client(client=client)
    wallet_id: int = await wallet.create_wallet(client_id=client_id)

    client: dict = dict(client.dict(), wallet_id=wallet_id, client_id=client_id)
    return client


async def create_client(client: serializers.ClientRequests) -> int:
    query = models.clients.insert().values(
        login=client.login,
        first_name=client.first_name,
        last_name=client.last_name,
        passport_series=client.passport_series,
        passport_number=client.passport_number,
    )
    try:
        client_id: int = await db.execute(query)
    except UniqueViolationError as ex:
        raise DuplicateClientExceptions(detail=ex.detail) from ex

    return client_id
