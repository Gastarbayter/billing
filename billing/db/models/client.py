import sqlalchemy as sa

from billing.db.engine import metadata


clients = sa.Table(
    'clients',
    metadata,
    sa.Column('client_id', sa.BigInteger, primary_key=True, autoincrement=True, nullable=False),
    sa.Column('login', sa.String, unique=True, nullable=False),
    sa.Column('first_name', sa.String, nullable=False),
    sa.Column('last_name', sa.String, nullable=False),
    sa.Column('passport_series', sa.String, nullable=False),
    sa.Column('passport_number', sa.Integer, nullable=False),
    sa.UniqueConstraint(
        'login',
        'first_name',
        'last_name',
        'passport_series',
        'passport_number',
        name='uniq_passport',
    ),
)
