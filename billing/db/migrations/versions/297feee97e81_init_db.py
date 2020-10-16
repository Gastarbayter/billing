"""init_db

Revision ID: 297feee97e81
Revises: 
Create Date: 2020-10-15 22:05:12.885047

"""
import uuid

import sqlalchemy as sa
from alembic import op
from sqlalchemy import func
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '297feee97e81'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'clients',
        sa.Column('client_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('login', sa.String, unique=True, nullable=False),
        sa.Column('first_name', sa.String, nullable=False),
        sa.Column('last_name', sa.String, nullable=False),
        sa.Column('passport_series', sa.String, nullable=False),
        sa.Column('passport_number', sa.String, nullable=False),

        sa.UniqueConstraint(
            'first_name',
            'last_name',
            'passport_series',
            'passport_number',
            name='uniq_passport',
        ),
    )

    op.create_table(
        'wallets',
        sa.Column('wallet_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('balance', sa.Numeric, nullable=False, default=0),
        sa.Column('client_id', sa.BigInteger, sa.ForeignKey('clients.client_id'), nullable=False, unique=True),
        sa.CheckConstraint('balance >= 0', name='check_balance')
    )

    op.create_table(
        'transactions',
        sa.Column('transaction_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column(
            'code',
            postgresql.UUID(),
            nullable=False,
            index=True,
            unique=True,
            default=uuid.uuid4(),
        )
    )
    op.create_table(
        'transactions_type',
        sa.Column('transaction_type_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
        sa.Column('type', sa.String, unique=True, nullable=False),
        sa.Column('label', sa.String, unique=True, nullable=False),
    )

    op.create_table(
        'transactions_history',
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
        sa.Column('transaction_date', sa.DateTime, server_default=func.now(), nullable=True),
    )


def downgrade():
    op.drop_table('transactions_history')
    op.drop_table('transactions_type')
    op.drop_table('transactions')
    op.drop_table('wallets')
    op.drop_table('clients')
