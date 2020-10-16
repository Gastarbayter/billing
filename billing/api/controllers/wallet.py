import typing as t
from decimal import Decimal

from asyncpg import CheckViolationError

from billing.db import models
from billing.db.engine import db
from billing.errors import exception


async def create_wallet(client_id: int) -> int:
    query = models.wallets.insert().values(client_id=client_id, balance=0)
    wallet_id: int = await db.execute(query)
    return wallet_id


async def change_balance(wallet_id: int, amount: Decimal) -> t.NoReturn:
    query = models.wallets.update()
    query = query.values(balance=models.wallets.c.balance + amount)
    query = query.where(models.wallets.c.wallet_id == wallet_id)
    query = query.returning(models.wallets.c.balance)

    try:
        balance: Decimal = await db.execute(query)
    except CheckViolationError as ex:
        raise exception.BalanceExceptions() from ex

    if balance is None:
        raise exception.WalletNotFoundExceptions(wallet_id=wallet_id)
    return balance
