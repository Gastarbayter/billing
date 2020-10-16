from decimal import Decimal

import pytest
from httpx import AsyncClient

from billing.app.fastapi import app as fast_api
from billing.db.engine import db
from billing.db.models import (
    clients,
    wallets,
)
from billing.db.models.transaction import (
    transactions_history,
    transactions,
)
from scripts import execute_migrations
from tests import raw_data


@pytest.fixture(autouse=True, scope='session')
def db_migrations():
    execute_migrations.upgrade()
    yield
    execute_migrations.downgrade()


@pytest.fixture()
async def db_connect():
    await db.connect()
    yield
    await db.disconnect()


@pytest.fixture()
async def create_clients_with_wallet():
    clients_id: list = []

    for client in raw_data.clients.clients:
        query = clients.insert().values(**client)
        client_id: int = await db.execute(query)

        query = wallets.insert().values(client_id=client_id, balance=Decimal(2000))
        wallet_id: int = await db.execute(query)
        clients_id.append(wallet_id)
    yield clients_id

    await db.execute(transactions_history.delete())
    await db.execute(transactions.delete())
    await db.execute(wallets.delete())
    await db.execute(clients.delete())


@pytest.fixture
async def fast_client():
    async with AsyncClient(app=fast_api, base_url="http://test/") as client:
        yield client
