import sqlalchemy as sa

from billing.db.engine import metadata


wallets = sa.Table(
    'wallets',
    metadata,
    sa.Column('wallet_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('balance', sa.Numeric, nullable=False, default=0),
    sa.Column('client_id', sa.BigInteger, sa.ForeignKey('clients.client_id'), nullable=False, unique=True),
    sa.CheckConstraint('balance >= 0', name='check_balance'),
)
