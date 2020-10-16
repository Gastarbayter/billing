import uuid

import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


transactions = sa.Table(
    'transactions',
    sa.Column(
        'transaction_id',
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
        unique=True,
        nullable=False,
    )
)

transactions_type = sa.Table(
    'transactions_type',
    sa.Column('transaction_type_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('type', sa.String, unique=True, nullable=False),
    sa.Column('label', sa.String, unique=True, nullable=False),
)

transactions_history = sa.Table(
    'transactions_history',
    sa.Column('transactions_history_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('wallet_id', sa.BigInteger, sa.ForeignKey('wallets.wallet_id'), nullable=False),
    sa.Column('transaction_id', UUID(as_uuid=True), sa.ForeignKey('transactions.transaction_id'), nullable=False),
    sa.Column(
        'transaction_type_id',
        sa.BigInteger,
        sa.ForeignKey('transactions_type.transaction_type_id'),
        nullable=False,
    ),
    sa.Column('amount', sa.Numeric, nullable=False),
    sa.Column('transaction_date', sa.DateTime(), nullable=True),
)
