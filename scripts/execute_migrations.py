import os

import alembic.command
import alembic.config

env = os.environ["ENVIRONMENT"].lower()

with open(f'config/{env}.env', 'r') as f:
    raw_config = f.readlines()
    config = dict([config_variable.strip().rsplit('=') for config_variable in raw_config if '=' in config_variable])

    DB_URL = '{drivername}://{user}:{password}@{host}:{port}/{database}'.format(
        drivername='postgresql',
        user=config['DB_USERNAME'],
        password=config['DB_PASSWORD'],
        host=config['DB_HOST'],
        port=config['DB_PORT'],
        database=config['DB_NAME'],
    )

alembic_cfg = alembic.config.Config()
alembic_cfg.set_main_option('script_location', 'billing/db/migrations')

alembic_cfg.set_main_option('sqlalchemy.url', DB_URL)


def upgrade():
    alembic.command.upgrade(alembic_cfg, 'head')


def downgrade():
    alembic.command.downgrade(alembic_cfg, 'base')


if __name__ == '__main__':
    upgrade()
