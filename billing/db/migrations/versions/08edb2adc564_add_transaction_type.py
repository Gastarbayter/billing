"""add transaction type

Revision ID: 08edb2adc564
Revises: 297feee97e81
Create Date: 2020-10-16 00:05:47.889007

"""
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.

revision = '08edb2adc564'
down_revision = '297feee97e81'
branch_labels = None
depends_on = None

meta = sa.MetaData(bind=op.get_bind())

transactions_type = sa.Table('transactions_type', meta)


def upgrade():
    op.execute("INSERT INTO transactions_type (type, label) VALUES ('TRANSFER', 'Перевод')")
    op.execute("INSERT INTO transactions_type (type, label) VALUES ('REPLENISHMENT', 'Пополнение кошелька клиента')")


def downgrade():
    op.execute("DELETE FROM transactions_type")
