import uuid
from decimal import Decimal

import pytest

from billing.api import (
    serializers,
    controllers,
)
from billing.api.controllers import wallet
from billing.api.controllers.client import create_client
from billing.api.serializers import (
    ReplenishmentRequests,
    TransferRequests,
)
from billing.db.engine import db
from billing.db.models.transaction import (
    transactions_type,
    transactions_history,
    transactions,
)
from billing.errors.exception import (
    BalanceExceptions,
    DuplicateClientExceptions,
)
from tests import raw_data


async def get_history_by_id_from_db(history_id: int) -> dict:
    query = transactions_history
    query = query.join(
        transactions_type,
        transactions_type.c.transaction_type_id == transactions_history.c.transaction_type_id
    )
    query = query.join(transactions, transactions.c.transaction_id == transactions_history.c.transaction_id)
    query = query.select()
    query = query.where(transactions_history.c.transactions_history_id == history_id)

    return dict(await db.fetch_one(query))


@pytest.mark.asyncio
async def test_negative_change_balance(db_connect, create_clients_with_wallet):
    with pytest.raises(BalanceExceptions) as ex:
        await wallet.change_balance(wallet_id=create_clients_with_wallet[0], amount=Decimal(-3000))

    assert ex.value.status_code == 400
    assert ex.value.message == 'Invalid client balance'


@pytest.mark.asyncio
async def test_create_duplicate_login(db_connect, create_clients_with_wallet):
    client = {
        **raw_data.clients.client_not_serialized,
        'lastName': 'New Last Name',
        'passportSeries': '0002',
    }
    client = serializers.ClientRequests(**client)
    with pytest.raises(DuplicateClientExceptions) as ex:
        await create_client(client=client)

    assert ex.value.status_code == 400
    assert ex.value.message == 'A client with this data already exists'


@pytest.mark.asyncio
async def test_create_duplicate_login(db_connect, create_clients_with_wallet):
    client = {
        **raw_data.clients.client_not_serialized,
        'login': 'New Login',
    }
    client = serializers.ClientRequests(**client)
    with pytest.raises(DuplicateClientExceptions) as ex:
        await create_client(client=client)

    assert ex.value.status_code == 400
    assert ex.value.message == 'A client with this data already exists'


@pytest.mark.asyncio
async def test_create_replenishment(db_connect, create_clients_with_wallet):
    amount: Decimal = Decimal(3000.55)
    code = uuid.uuid4()
    replenishment = ReplenishmentRequests(
        **{
            'transactionCode': code,
            "amount": amount,
            "walletId": create_clients_with_wallet[0]
        },
    )
    result: dict = await controllers.create_replenishment(replenishment=replenishment)

    result_db: dict = await get_history_by_id_from_db(history_id=result['history_id'])

    assert result['wallet_id'] == result_db['target_wallet_id']
    assert result['transaction_code'] == result_db['code'] == code
    assert result['transaction_type_id'] == result_db['transaction_type_id']
    assert result['amount'] == result_db['amount'] == amount


@pytest.mark.asyncio
async def test_create_transfer(db_connect, create_clients_with_wallet):
    amount: Decimal = Decimal(1000)
    code = uuid.uuid4()
    transfer = TransferRequests(
        **{
            'transactionCode': code,
            "amount": amount,
            "sourceWalletId": create_clients_with_wallet[0],
            "targetWalletId": create_clients_with_wallet[1]
        })
    result: dict = await controllers.create_transfer(transfer=transfer)

    result_db: dict = await get_history_by_id_from_db(history_id=result['history_id'])

    assert result['source_wallet_id'] == result_db['source_wallet_id']
    assert result['target_wallet_id'] == result_db['target_wallet_id']
    assert result['transaction_code'] == result_db['code'] == code
    assert result['transaction_type_id'] == result_db['transaction_type_id']
    assert result['amount'] == result_db['amount'] == amount
