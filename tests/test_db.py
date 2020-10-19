from decimal import Decimal
from uuid import UUID

import pytest
from asyncpg import (
    CheckViolationError,
    UniqueViolationError,
)

from billing.db import models
from billing.db.engine import db
from billing.db.models import (
    wallets,
    clients,
)
from billing.db.models.transaction import transactions
from tests import raw_data


@pytest.mark.asyncio
async def test_create_wallet_negative_balance_in_db(db_connect):
    query = clients.insert().values(**raw_data.clients.clients[0])
    client_id: int = await db.execute(query)

    query = wallets.insert().values(client_id=client_id, balance=Decimal(-1))

    with pytest.raises(CheckViolationError) as ex:
        await db.execute(query)
    assert ex.value.constraint_name == 'check_balance'
    assert ex.value.message == 'new row for relation "wallets" violates check constraint "check_balance"'

    await db.execute(wallets.delete())
    await db.execute(clients.delete())


@pytest.mark.asyncio
async def test_negative_change_balance_in_db(db_connect, create_clients_with_wallet):
    query = models.wallets.update()
    query = query.values(balance=models.wallets.c.balance - Decimal(3000))
    query = query.where(models.wallets.c.wallet_id == create_clients_with_wallet[0])
    query = query.returning(models.wallets.c.balance)

    with pytest.raises(CheckViolationError) as ex:
        await db.execute(query)

    assert ex.value.constraint_name == 'check_balance'
    assert ex.value.message == 'new row for relation "wallets" violates check constraint "check_balance"'


@pytest.mark.asyncio
async def test_create_duplicate_login_in_db(db_connect, create_clients_with_wallet):
    client = {
        **raw_data.clients.clients[0],
        'last_name': 'New Last Name',
        'passport_series': '0002',
    }
    query = clients.insert().values(**client)

    with pytest.raises(UniqueViolationError) as ex:
        await db.execute(query)

    assert ex.value.constraint_name == 'clients_login_key'
    assert ex.value.message == 'duplicate key value violates unique constraint "clients_login_key"'


@pytest.mark.asyncio
async def test_create_duplicate_passport_data_in_db(db_connect, create_client_with_wallet):
    client = {
        **raw_data.clients.client,
        'login': 'New Login',
    }
    query = clients.insert().values(**client)

    with pytest.raises(UniqueViolationError) as ex:
        await db.execute(query)

    assert ex.value.constraint_name == 'uniq_passport'
    assert ex.value.message == 'duplicate key value violates unique constraint "uniq_passport"'


@pytest.mark.asyncio
async def test_create_duplicate_passport_data_in_db(db_connect, create_clients_with_wallet):
    client = {
        **raw_data.clients.clients[0],
        'login': 'New Login',
    }
    query = clients.insert().values(**client)

    with pytest.raises(UniqueViolationError) as ex:
        await db.execute(query)

    assert ex.value.constraint_name == 'uniq_passport'
    assert ex.value.message == 'duplicate key value violates unique constraint "uniq_passport"'


@pytest.mark.asyncio
async def test_create_duplicate_transaction_code_db(db_connect):

    code = UUID("3fa85f64-5717-4562-b3fc-2c963f66afa9")
    query = transactions.insert().values(code=code)

    await db.execute(query)

    with pytest.raises(Exception) as ex:
        await db.execute(query)

    assert ex.value.constraint_name == 'ix_transactions_code'
    assert ex.value.message == 'duplicate key value violates unique constraint "ix_transactions_code"'