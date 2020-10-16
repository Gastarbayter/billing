import databases
import sqlalchemy
from sqlalchemy import MetaData
from sqlalchemy.engine import Engine

from billing.app.config import settings

metadata: MetaData = MetaData()
engine: Engine = sqlalchemy.create_engine(settings.DB_URL)
metadata.create_all(engine)

db = databases.Database(settings.DB_URL)
