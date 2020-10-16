from unittest.mock import patch

import pytest
from asynctest import CoroutineMock
from httpx import AsyncClient

from billing.errors.exception import (
    DuplicateClientExceptions,
    BalanceExceptions,
    WalletNotFoundExceptions,
)
from tests.raw_data import (
    clients,
    transfers,
    replenishments,
)


@pytest.mark.asyncio
@pytest.mark.parametrize('client', clients.new_clients)
async def test_create_client(client: dict, fast_client: AsyncClient):
    with patch(
        "billing.api.controllers.create_client_with_wallet",
        new=CoroutineMock(return_value=client['mock_response'])
    ) as create_client_mock:
        response = await fast_client.post('v1/clients', json=client['request'])

    assert response.status_code == 201
    assert create_client_mock.called
    assert dict(create_client_mock.await_args.kwargs['client']) == client['call_kwargs']
    assert response.json() == client['response']


@pytest.mark.asyncio
@pytest.mark.parametrize('client', clients.new_clients)
async def test_create_client_duplicate_login(client: dict, fast_client: AsyncClient):
    with patch(
        'billing.api.controllers.create_client_with_wallet',
        new=CoroutineMock(side_effect=DuplicateClientExceptions())
    ) as create_client_mock:
        response = await fast_client.post('v1/clients', json=client['request'])

    assert response.status_code == 400
    assert create_client_mock.called
    assert dict(create_client_mock.await_args.kwargs['client']) == client['call_kwargs']
    assert response.json() == {'detail': None, 'message': 'A client with this data already exists'}


@pytest.mark.asyncio
@pytest.mark.parametrize('client', clients.invalid_clients)
async def test_create_client_not_valid(client: dict, fast_client: AsyncClient):
    response = await fast_client.post('v1/clients', json=client['request'])

    assert response.status_code == 422
    assert response.json() == client['response']


@pytest.mark.asyncio
@pytest.mark.parametrize('transfer', transfers.new_transfers)
async def test_create_transfer(transfer: dict, fast_client: AsyncClient):
    with patch(
        "billing.api.controllers.create_transfer",
        new=CoroutineMock(return_value=transfer['mock_response'])
    ) as create_transfer_mock:
        response = await fast_client.post('v1/transfer', json=transfer['request'])

    assert response.status_code == 201
    assert create_transfer_mock.called
    assert response.json() == transfer['response']


@pytest.mark.asyncio
@pytest.mark.parametrize('transfer', transfers.new_transfers)
async def test_create_transfer_not_valid_balance(transfer: dict, fast_client: AsyncClient):
    with patch(
        'billing.api.controllers.create_transfer',
        new=CoroutineMock(side_effect=BalanceExceptions())
    ) as create_transfer_mock:
        response = await fast_client.post('v1/transfer', json=transfer['request'])

    assert response.status_code == 400
    assert create_transfer_mock.called
    assert response.json() == {'detail': None, 'message': 'Invalid client balance'}


@pytest.mark.asyncio
@pytest.mark.parametrize('transfer', transfers.new_transfers)
async def test_create_transfer_not_valid_wallet(transfer: dict, fast_client: AsyncClient):
    wallet_id = transfer['request']['sourceWalletId']
    with patch(
        'billing.api.controllers.create_transfer',
        new=CoroutineMock(side_effect=WalletNotFoundExceptions(wallet_id=wallet_id))
    ) as create_transfer_mock:
        response = await fast_client.post('v1/transfer', json=transfer['request'])

    assert response.status_code == 404
    assert create_transfer_mock.called
    assert response.json() == {'detail': None, 'message': f'Wallet id: {wallet_id} not found'}


@pytest.mark.asyncio
@pytest.mark.parametrize('transfer', transfers.invalid_transfers)
async def test_create_transfer_not_valid(transfer: dict, fast_client: AsyncClient):
    response = await fast_client.post('v1/transfer', json=transfer['request'])

    assert response.status_code == 422
    assert response.json() == transfer['response']


@pytest.mark.asyncio
@pytest.mark.parametrize('replenishment', replenishments.new_replenishments)
async def test_create_replenishment(replenishment: dict, fast_client: AsyncClient):
    with patch(
        "billing.api.controllers.create_replenishment",
        new=CoroutineMock(return_value=replenishment['mock_response'])
    ) as create_replenishment_mock:
        response = await fast_client.post('v1/replenishment', json=replenishment['request'])

    assert response.status_code == 201
    assert create_replenishment_mock.called
    assert response.json() == replenishment['response']


@pytest.mark.asyncio
@pytest.mark.parametrize('replenishment', replenishments.new_replenishments)
async def test_create_replenishment_not_valid_wallet(replenishment: dict, fast_client: AsyncClient):
    wallet_id = replenishment['request']['walletId']
    with patch(
        'billing.api.controllers.create_replenishment',
        new=CoroutineMock(side_effect=WalletNotFoundExceptions(wallet_id=wallet_id))
    ) as create_replenishment_mock:
        response = await fast_client.post('v1/replenishment', json=replenishment['request'])

    assert response.status_code == 404
    assert create_replenishment_mock.called
    assert response.json() == {'detail': None, 'message': f'Wallet id: {wallet_id} not found'}


@pytest.mark.asyncio
@pytest.mark.parametrize('replenishment', replenishments.invalid_replenishments)
async def test_create_replenishment_not_valid(replenishment: dict, fast_client: AsyncClient):
    response = await fast_client.post('v1/replenishment', json=replenishment['request'])

    assert response.status_code == 422
    assert response.json() == replenishment['response']
