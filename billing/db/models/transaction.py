import typing as t
from decimal import Decimal

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

from billing.api import serializers
from billing.db.engine import (
    metadata,
    db,
)
from billing.utils.constances import TransactionType

transactions = sa.Table(
    'transactions',
    metadata,
    sa.Column('transaction_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('code', UUID(as_uuid=True), unique=True, nullable=False),
)

transactions_type = sa.Table(
    'transactions_type',
    metadata,
    sa.Column('transaction_type_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('type', sa.String, unique=True, nullable=False),
    sa.Column('label', sa.String, unique=True, nullable=False),
)

transactions_history = sa.Table(
    'transactions_history',
    metadata,
    sa.Column('transactions_history_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('source_wallet_id', sa.BigInteger, sa.ForeignKey('wallets.wallet_id'), nullable=True),
    sa.Column('target_wallet_id', sa.BigInteger, sa.ForeignKey('wallets.wallet_id'), nullable=False),
    sa.Column('transaction_id', sa.BigInteger, sa.ForeignKey('transactions.transaction_id'), nullable=False),
    sa.Column(
        'transaction_type_id',
        sa.BigInteger,
        sa.ForeignKey('transactions_type.transaction_type_id'),
        nullable=False,
    ),
    sa.Column('amount', sa.DECIMAL, nullable=False),
    sa.Column('transaction_date', sa.DateTime, nullable=True),
)


class Transactions:

    @staticmethod
    async def is_contains_transaction(code: UUID) -> bool:
        query = transactions.select().where(transactions.c.code == code)
        transaction = await db.fetch_one(query)

        return transaction is not None

    @staticmethod
    async def save_transaction(code: UUID) -> int:
        query = transactions.insert().values(code=str(code))
        transaction_id: int = await db.execute(query)
        return transaction_id

    @staticmethod
    async def save_history(
        target_wallet_id: int,
        transaction_type_id: int,
        code:UUID,
        amount: Decimal,
        source_wallet_id: int = None,
    ) -> int:
        transaction_id: int = await Transactions.save_transaction(code=code)

        query = transactions_history.insert().values(
            source_wallet_id=source_wallet_id,
            target_wallet_id=target_wallet_id,
            transaction_id=transaction_id,
            transaction_type_id=transaction_type_id,
            amount=amount,
        )
        history_id: int = await db.execute(query)
        return history_id

    @staticmethod
    async def get_transaction_type(transaction_type: TransactionType) -> dict:
        query = transactions_type.select()
        query = query.where(transactions_type.c.type == transaction_type.value)
        transaction_type = await db.fetch_one(query)
        return dict(transaction_type)
